import pytest
import subprocess

from utils import *
from client.core.config import ClientConfig

# TODO: make class with constant data used in multiple tests


# service fixtures

# client fixtures
@pytest.fixture
def mock_update_client_status(monkeypatch):
    monkeypatch.setattr(ClientConfig, "update_client_status", lambda *args, **kwargs: None)


# utils fixtures
@pytest.fixture
def mock_subprocess_popen(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', lambda *args, **kwargs: None)


@pytest.fixture
def mock_files_management(monkeypatch):
    def mock_set_data(*args, **kwargs):
        # TODO: implement
        pass

    monkeypatch.setattr(FilesManagement, '_set_data', mock_set_data)
    monkeypatch.setattr(FilesManagement, 'overwrite', lambda *args, **kwargs: None)
    monkeypatch.setattr(FilesManagement, 'clear', lambda *args, **kwargs: None)
    monkeypatch.setattr(FilesManagement, 'write_line', lambda *args, **kwargs: None)
