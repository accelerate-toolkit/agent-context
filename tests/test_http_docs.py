"""HTTP snapshots preserve usable evidence across failed refreshes."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_hydrate_cached_docs import hydrator


class HttpDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'cached-docs.yml'
        self.cache = self.root / '.agent-cache'
        self.files = [{'url': 'https://docs.example.test/guide.md',
                       'destination': 'guide.md', 'format': 'markdown'}]

    def source(self, files=None):
        self.manifest.write_text(hydrator.yaml.safe_dump({'cached_docs': [
            {'id': 'example', 'strategy': {'type': 'http-files'},
             'files': files if files is not None else self.files}]}))
        return hydrator.load_sources(self.manifest)[0]

    @staticmethod
    def download(url, target):
        target.write_bytes(b'%PDF-example' if url.endswith('.pdf') else b'# Reference\n')
        return {'resolved_url': url, 'headers': {'ETag': 'example'}}

    def hydrate(self, source):
        with patch.object(hydrator, 'download_http', side_effect=self.download):
            hydrator.hydrate(source, self.cache, False)
        return (self.cache / 'tool-docs/example/current').resolve()

    def test_snapshot_provenance_integrity_and_repeat(self):
        source = self.source()
        first = self.hydrate(source)
        with patch.object(hydrator, 'download_http', side_effect=AssertionError('offline')):
            hydrator.check_http_cache(source, self.cache)
        metadata = json.loads((first / 'provenance.json').read_text())
        self.assertEqual(metadata['files'][0]['url'], self.files[0]['url'])
        self.assertEqual(metadata['files'][0]['headers']['ETag'], 'example')
        second = self.hydrate(source)
        self.assertNotEqual(first, second)
        self.assertTrue((first / 'guide.md').is_file())
        (second / 'guide.md').write_text('modified')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            hydrator.check_http_cache(source, self.cache)

    def test_failed_download_retains_current_and_cleans_staging(self):
        source = self.source()
        first = self.hydrate(source)
        with patch.object(hydrator, 'download_http', side_effect=OSError('offline')):
            with self.assertRaises(OSError):
                hydrator.hydrate(source, self.cache, False)
        self.assertEqual((first.parent / 'current').resolve(), first)
        self.assertFalse(list(first.parent.glob('.download-*')))

    def test_rejects_html_and_empty_without_publishing(self):
        source = self.source()
        for data in (b'<html>error</html>', b''):
            with self.subTest(data=data):
                def bad_download(url, target):
                    target.write_bytes(data)
                    return {}
                with patch.object(hydrator, 'download_http', side_effect=bad_download):
                    with self.assertRaises(ValueError):
                        hydrator.hydrate(source, self.cache, False)
                self.assertFalse((self.cache / 'tool-docs/example/current').exists())

    def test_pdf_extraction_and_failure_preserve_snapshot(self):
        source = self.source([{'url': 'https://docs.example.test/guide.pdf',
                              'destination': 'guide.pdf', 'format': 'pdf',
                              'text_destination': 'search/guide.txt'}])
        def extract(command, **kwargs):
            if '-layout' in command:
                Path(command[-1]).write_text('Searchable PDF content')
            return subprocess.CompletedProcess(command, 0, '', 'pdftotext test')
        with patch.object(hydrator.subprocess, 'run', side_effect=extract):
            first = self.hydrate(source)
        self.assertEqual((first / 'search/guide.txt').read_text(), 'Searchable PDF content')
        hydrator.check_http_cache(source, self.cache)
        def fail_extraction(command, **kwargs):
            if '-layout' in command:
                raise subprocess.CalledProcessError(1, command)
            return extract(command, **kwargs)
        with patch.object(hydrator.subprocess, 'run', side_effect=fail_extraction):
            with self.assertRaises(subprocess.CalledProcessError):
                self.hydrate(source)
        self.assertEqual((first.parent / 'current').resolve(), first)

    def test_invalid_pdf_not_published(self):
        source = self.source([{'url': 'https://docs.example.test/invalid',
                              'destination': 'guide.pdf', 'format': 'pdf'}])
        with self.assertRaisesRegex(ValueError, 'Expected PDF'):
            self.hydrate(source)

    def test_manifest_rejects_paths_collisions_and_bad_urls(self):
        bad_files = [
            [dict(self.files[0], destination='../escape')],
            [dict(self.files[0], destination='/absolute')],
            [dict(self.files[0], destination='provenance.json')],
            [dict(self.files[0], url='http://docs.example.test/guide')],
            [dict(self.files[0], url='https://user:secret@docs.example.test/guide')],
            [self.files[0], self.files[0]],
            [dict(self.files[0], destination='folder'), dict(self.files[0], destination='folder/page')],
            [dict(self.files[0], text_destination='guide.txt')],
            [dict(self.files[0], format='html')],
        ]
        for files in bad_files:
            with self.subTest(files=files), self.assertRaises(ValueError):
                self.source(files)

    def test_dry_run_is_offline_and_does_not_write(self):
        with patch.object(hydrator, 'download_http', side_effect=AssertionError('network')):
            hydrator.hydrate(self.source(), self.cache, True)
        self.assertFalse(self.cache.exists())

    def test_redirect_rejects_http_downgrade(self):
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            hydrator.HTTPSRedirectHandler().redirect_request(
                None, None, 302, '', {}, 'http://docs.example.test/guide')

    def test_missing_configured_file_fails_check(self):
        source = self.source()
        self.hydrate(source)
        source = self.source(self.files + [dict(self.files[0], destination='new.md')])
        with self.assertRaisesRegex(ValueError, 'missing configured'):
            hydrator.check_http_cache(source, self.cache)

    def test_missing_pdf_tool_fails_before_download(self):
        source = self.source([{'url': 'https://docs.example.test/guide.pdf',
                              'destination': 'guide.pdf', 'format': 'pdf',
                              'text_destination': 'guide.txt'}])
        with patch.object(hydrator.subprocess, 'run', side_effect=FileNotFoundError), \
             patch.object(hydrator, 'download_http') as download:
            with self.assertRaises(FileNotFoundError):
                hydrator.hydrate(source, self.cache, False)
            download.assert_not_called()
