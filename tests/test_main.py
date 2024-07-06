import pytest
import pdf2doi
import tempfile
import fitz
from pathlib import Path
import logging
import os
import pdf2doi.config as config
import subprocess, shlex


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
test_identifier_type = "DOI"
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


def test_execution_from_cli(pdf_path):
    cmd = f'pdf2doi "{str(pdf_path)}"'
    result = subprocess.run(shlex.split(cmd), check=True, capture_output=True)
    assert result.returncode == 0
    identifier_type, identifier, *_ = result.stdout.decode().split()
    assert identifier_type == test_identifier_type
    assert identifier == test_doi.lower()
