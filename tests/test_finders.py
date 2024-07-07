import pytest
import pdf2doi
import tempfile
import fitz
from pathlib import Path
import logging
import os
import pdf2doi.config as config

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

valid_test_doi = r"10.1103/PhysRev.47.777".lower()
valid_test_title = (
    r"Can Quantum Mechanical Description of Physical Reality Be Considered Complete"
)
wrong_test_doi = "foo"
valid_arxiv_id = r"arXiv:acc-phys/9601001"


@pytest.fixture
def valid_pdf_path(tmp_path):
    file_path = tmp_path / (
        valid_test_doi.replace("/", r"%2F") + " " + valid_test_title + ".pdf"
    )
    doc = fitz.open()
    doc.insert_page(-1, text=(valid_test_doi + " " + valid_test_title))
    doc.save(file_path)
    doc.close()
    return file_path


@pytest.fixture
def wrong_pdf_path(tmp_path):
    file_path = tmp_path / (wrong_test_doi + ".pdf")
    doc = fitz.open()
    doc.insert_page(-1, text=(wrong_test_doi))
    doc.save(file_path)
    doc.close()
    return file_path


def test_validate_doi_web():
    r = pdf2doi.finders.validate_doi_web(valid_test_doi)
    assert isinstance(r, str)

    r = pdf2doi.finders.validate_doi_web(wrong_test_doi)
    assert r is None


def test_read_pdf_info(valid_pdf_path):

    assert valid_pdf_path.exists()

    pdf2doi.finders.add_found_identifier_to_metadata(
        target=str(valid_pdf_path), identifier="test"
    )

    with open(valid_pdf_path, "rb") as f:
        info = pdf2doi.finders.get_pdf_info(f)

    assert info is not None


def test_find_identifier_in_pdf_info(valid_pdf_path):

    assert valid_pdf_path.exists()

    pdf2doi.finders.add_found_identifier_to_metadata(
        target=str(valid_pdf_path), identifier=valid_test_doi
    )

    with open(valid_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_info(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == valid_test_doi


def test_find_identifier_in_pdf_text(valid_pdf_path):

    assert valid_pdf_path.exists()

    with open(valid_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == valid_test_doi


def test_find_identifier_in_pdf_text_fail(wrong_pdf_path):

    assert wrong_pdf_path.exists()

    with open(wrong_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_pdf_text(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier is None


def test_find_identifier_in_filename(valid_pdf_path):

    assert valid_pdf_path.exists()

    with open(valid_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_filename(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == valid_test_doi


def test_find_identifier_in_filename_fail(wrong_pdf_path):

    assert wrong_pdf_path.exists()

    with open(wrong_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_in_filename(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier is None


def test_find_identifier_by_googling_title(valid_pdf_path):

    assert valid_pdf_path.exists()

    with open(valid_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_by_googling_title(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier == valid_test_doi


def test_find_identifier_by_googling_title_fail(wrong_pdf_path):

    assert wrong_pdf_path.exists()

    with open(wrong_pdf_path, "rb") as f:
        identifier, desc, info = pdf2doi.find_identifier_by_googling_title(
            f, func_validate=pdf2doi.finders.validate
        )

    assert identifier is None


def test_find_identifier_by_googling_first_N_characters_in_pdf(valid_pdf_path):

    assert valid_pdf_path.exists()

    with open(valid_pdf_path, "rb") as f:
        identifier, desc, info = (
            pdf2doi.find_identifier_by_googling_first_N_characters_in_pdf(
                f, func_validate=pdf2doi.finders.validate
            )
        )

    assert identifier == valid_test_doi


def test_find_identifier_by_googling_first_N_characters_in_pdf_fail(wrong_pdf_path):

    assert wrong_pdf_path.exists()

    with open(wrong_pdf_path, "rb") as f:
        identifier, desc, info = (
            pdf2doi.find_identifier_by_googling_first_N_characters_in_pdf(
                f, func_validate=pdf2doi.finders.validate
            )
        )

    assert identifier is None


if __name__ == "__main__":
    pass
