"""HTTP snapshots preserve usable evidence across failed refreshes."""
import json
from pathlib import Path
import io
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
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

    @staticmethod
    def pdf_bytes(pages=("First page content", "Second page content"), encrypted=False):
        writer = PdfWriter()
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        for text in pages:
            page = writer.add_blank_page(width=600, height=800)
            page[NameObject('/Resources')] = DictionaryObject({
                NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
            stream = DecodedStreamObject()
            stream.set_data(f'BT /F1 12 Tf 50 750 Td ({text}) Tj ET'.encode())
            page[NameObject('/Contents')] = stream
        if encrypted:
            writer.encrypt('secret')
        output = io.BytesIO()
        writer.write(output)
        return output.getvalue()

    def pdf_source(self):
        return self.source([{'url': 'https://docs.example.test/guide.pdf',
                             'destination': 'guide.pdf', 'format': 'pdf',
                             'text_destination': 'search/guide.txt'}])

    def hydrate_pdf(self, source, data):
        def download(url, target):
            target.write_bytes(data)
            return {'resolved_url': url}
        with patch.object(hydrator, 'download_http', side_effect=download):
            hydrator.hydrate(source, self.cache, False)
        return (self.cache / 'tool-docs/example/current').resolve()

    def test_pdf_extraction_preserves_bytes_pages_and_provenance(self):
        source = self.pdf_source()
        data = self.pdf_bytes()
        first = self.hydrate_pdf(source, data)
        self.assertEqual((first / 'guide.pdf').read_bytes(), data)
        text = (first / 'search/guide.txt').read_text()
        self.assertIn('First page content', text.split('\f')[0])
        self.assertIn('Second page content', text.split('\f')[1])
        metadata = json.loads((first / 'provenance.json').read_text())
        self.assertEqual(metadata['pdf_extractor']['name'], 'pypdf')
        self.assertEqual(metadata['pdf_extractor']['version'], hydrator.pypdf.__version__)
        hydrator.check_http_cache(source, self.cache)
        second = self.hydrate_pdf(source, data)
        self.assertNotEqual(first, second)
        (second / 'search/guide.txt').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            hydrator.check_http_cache(source, self.cache)

    def test_pdf_failures_preserve_snapshot_and_clean_staging(self):
        source = self.pdf_source()
        first = self.hydrate_pdf(source, self.pdf_bytes())
        for data in (b'%PDF-invalid', self.pdf_bytes()[:-30],
                     self.pdf_bytes(pages=('   ',)), self.pdf_bytes(encrypted=True)):
            with self.subTest(data=data[:20]):
                with self.assertRaises((ValueError, hydrator.pypdf.errors.PyPdfError)):
                    self.hydrate_pdf(source, data)
                self.assertEqual((first.parent / 'current').resolve(), first)
                self.assertFalse(list(first.parent.glob('.download-*')))
                self.assertEqual(len(list(first.parent.iterdir())), 2)
                hydrator.check_http_cache(source, self.cache)

    def test_legacy_poppler_snapshot_remains_verifiable(self):
        source = self.pdf_source()
        first = self.hydrate_pdf(source, self.pdf_bytes())
        path = first / 'provenance.json'
        metadata = json.loads(path.read_text())
        metadata.pop('pdf_extractor')
        metadata['pdftotext_version'] = 'pdftotext legacy'
        path.write_text(json.dumps(metadata))
        sums = first / 'SHA256SUMS'
        sums.write_text(''.join(
            f"{hydrator.file_hash(first / line.split('  ', 1)[1])}  {line.split('  ', 1)[1]}\n"
            for line in sums.read_text().splitlines()))
        original = path.read_bytes()
        hydrator.check_http_cache(source, self.cache)
        self.hydrate_pdf(source, self.pdf_bytes())
        self.assertEqual(path.read_bytes(), original)

    def test_incomplete_download_is_rejected(self):
        response = io.BytesIO(b'partial')
        response.headers = {'Content-Length': '100'}
        response.url = 'https://docs.example.test/guide.pdf'
        with patch.object(hydrator.urllib.request, 'build_opener') as opener:
            opener.return_value.open.return_value = response
            with self.assertRaisesRegex(ValueError, 'Incomplete download'):
                hydrator.download_http(response.url, self.root / 'partial.pdf')

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
