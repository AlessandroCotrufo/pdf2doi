import pytest
import pdf2doi
import tempfile
import fitz
from pathlib import Path
import logging
import os
import pdf2doi.config as config


logger = logging.getLogger("pdf2doi")

default_config_params = {
    "verbose": True,
    "separator": os.path.sep,
    "method_dxdoiorg": "application/citeproc+json",
    "webvalidation": True,
    "websearch": True,
    "numb_results_google_search": 6,
    "N_characters_in_pdf": 1000,
    "save_identifier_metadata": True,
    "replace_arxivID_by_DOI_when_available": True,
}

config.update_params(default_config_params)

test_doi = r"10.1103/PhysRev.47.777"
test_title = (
    r"Can Quantum Mechanical Description of Physical Reality Be Considered Complete"
)


@pytest.fixture
def pdf_path(tmp_path):
    file_path = tmp_path / (test_title + ".pdf")
    doc = fitz.open()
    doc.insert_page(-1, text=(test_doi + " " + test_title))
    doc.save(file_path)
    doc.close()
    return file_path


def test_read_pdf_info(pdf_path):

    assert pdf_path.exists()

    pdf2doi.finders.add_found_identifier_to_metadata(
        target=str(pdf_path), identifier="test"
    )

    with open(pdf_path, "rb") as f:
        info = pdf2doi.finders.get_pdf_info(f)

    assert info is not None


def test_find_identifier_in_pdf_info(pdf_path):

    assert pdf_path.exists()

    pdf2doi.finders.add_found_identifier_to_metadata(
        target=str(pdf_path), identifier=test_doi
    )

    with open(pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_info(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == test_doi.lower()


def test_find_identifier_in_pdf_text(pdf_path):

    assert pdf_path.exists()

    with open(pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == test_doi.lower()


def test_find_identifier_in_filename(pdf_path):

    assert pdf_path.exists()

    with open(pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == test_doi.lower()


def test_find_identifier_by_googling_title(pdf_path):

    assert pdf_path.exists()

    with open(pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_by_googling_title(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == test_doi.lower()


def test_find_identifier_by_googling_first_N_characters_in_pdf(pdf_path):

    assert pdf_path.exists()

    with open(pdf_path, "rb") as f:
        identifier, desc, info = (
            pdf2doi.find_identifier_by_googling_first_N_characters_in_pdf(
                f, func_validate=pdf2doi.finders.validate
            )
        )

    assert identifier == test_doi.lower()


if __name__ == "__main__":
    pass
