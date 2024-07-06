import pytest
import pdf2doi
import tempfile
import fitz
from pathlib import Path
import logging

logger = logging.getLogger("pdf2doi")


def test_read_pdf_info():

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / "foo.pdf"

        doc = fitz.open()
        doc.insert_page(-1, text="Lorem ipsum")
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        pdf2doi.finders.add_found_identifier_to_metadata(
            target=str(pdf_path), identifier="test"
        )

        with open(pdf_path, "rb") as f:
            info = pdf2doi.finders.get_pdf_info(f)

        assert info is not None


def test_find_identifier_in_pdf_info():

    test_doi = "10.1103/PhysRev.47.777"

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / "foo.pdf"

        doc = fitz.open()
        doc.insert_page(-1, text="Lorem ipsum")
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        pdf2doi.finders.add_found_identifier_to_metadata(
            target=str(pdf_path), identifier=test_doi
        )

        with open(pdf_path, "rb") as f:
            identifier, desc, info = pdf2doi.find_identifier_in_pdf_info(
                f, func_validate=pdf2doi.finders.validate
            )

    assert identifier == test_doi.lower()


def test_find_identifier_in_pdf_text():
    test_doi = "10.1103/PhysRev.47.777"

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / "foo.pdf"

        doc = fitz.open()
        doc.insert_page(-1, text=test_doi)
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        with open(pdf_path, "rb") as f:
            identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
                f, func_validate=pdf2doi.finders.validate
            )

    assert identifier == test_doi.lower()


def test_find_identifier_in_filename():
    test_doi = "10.1103/PhysRev.47.777"

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / "foo.pdf"

        doc = fitz.open()
        doc.insert_page(-1, text=test_doi)
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        with open(pdf_path, "rb") as f:
            identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
                f, func_validate=pdf2doi.finders.validate
            )

    assert identifier == test_doi.lower()


def test_find_identifier_by_googling_title():
    pdf_title = (
        "Can Quantum Mechanical Description of Physical Reality Be Considered Complete"
    )
    test_doi = "10.1103/PhysRev.47.777"

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / pdf_title

        doc = fitz.open()
        doc.insert_page(-1, text="Lorem ipsum")
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        with open(pdf_path, "rb") as f:
            identifier, desc, info = pdf2doi.find_identifier_by_googling_title(
                f, func_validate=pdf2doi.finders.validate
            )

    assert identifier == test_doi.lower()


def test_find_identifier_by_googling_first_N_characters_in_pdf():
    pdf_text = (
        "Can Quantum Mechanical Description of Physical Reality Be Considered Complete"
    )
    test_doi = "10.1103/PhysRev.47.777"

    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_path = Path(tmpdirname) / "foo.txt"

        doc = fitz.open()
        doc.insert_page(-1, text=pdf_text)
        doc.save(pdf_path)
        doc.close()

        assert pdf_path.exists()

        with open(pdf_path, "rb") as f:
            identifier, desc, info = pdf2doi.find_identifier_by_googling_title(
                f, func_validate=pdf2doi.finders.validate
            )

    assert identifier == test_doi.lower()


if __name__ == "__main__":
    pass
