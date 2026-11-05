"""Check extraction with real PDF streams and reproducible output."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

spec = importlib.util.spec_from_file_location(
    "pdf_reference", Path(__file__).resolve().parents[1] / "scripts/extract_pdf_reference.py")
pdf_reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pdf_reference)


class PdfReferenceTests(unittest.TestCase):
    def test_text_pages_and_repeat_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.pdf"
            writer = PdfWriter()
            font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                     NameObject('/Subtype'): NameObject('/Type1'),
                                     NameObject('/BaseFont'): NameObject('/Helvetica')})
            for text in ('First searchable page', 'Second searchable page'):
                page = writer.add_blank_page(612, 792)
                page[NameObject('/Resources')] = DictionaryObject({
                    NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
                stream = DecodedStreamObject()
                stream.set_data(f'BT /F1 12 Tf 50 700 Td ({text}) Tj ET'.encode())
                page[NameObject('/Contents')] = stream
            writer.write(path)
            args = (path, 'Reference', 'https://example.test/reference.pdf', '2026')
            result = pdf_reference.render_reference(*args)
            self.assertIn('First searchable page', result)
            self.assertIn('Second searchable page', result)
            self.assertIn('[Page 2](#page-2)', result)
            self.assertIn('Source PDF SHA-256:', result)
            self.assertEqual(result, pdf_reference.render_reference(*args))

    def test_empty_pdf_requires_manual_preparation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'blank.pdf'
            writer = PdfWriter()
            writer.add_blank_page(612, 792)
            writer.write(path)
            with self.assertRaisesRegex(ValueError, 'no extractable text'):
                pdf_reference.render_reference(path, 'Blank', 'https://example.test/blank.pdf', '2026')
