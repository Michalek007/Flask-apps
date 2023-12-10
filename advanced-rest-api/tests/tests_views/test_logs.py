import pytest

from request_context import RequestContext
from app.blueprints.logs.logs_class import LogsClass
from app.blueprints.logs.modules import LogsHandler
from tests.conftest import mock_files_management
from utils import FilesManagement


class TestLogs:
    # requests
    def get_logs(self, name: str):
        return RequestContext.request('/get_logs/', LogsClass(), LogsClass.get_logs, arg=name)

    def delete_logs(self, name: str, **kwargs):
        return RequestContext.request('/delete_logs/', LogsClass(), LogsClass.delete_logs, arg=name, query_string=kwargs)

    # private fixtures
    @pytest.fixture
    def mock_logs_handler(self, monkeypatch):
        monkeypatch.setattr(LogsHandler, 'delete', lambda *args, **kwargs: None)
        monkeypatch.setattr(LogsHandler, 'get', lambda *args, **kwargs: None)

    @pytest.fixture
    def mock_files_management_set_data(self, monkeypatch, mock_files_management):
        def mock_set_data(*args, **kwargs):
            args[0].data = ['log1', 'log2', 'log3']
        monkeypatch.setattr(FilesManagement, '_set_data', mock_set_data)

    @pytest.fixture
    def mock_files_management_file_not_found(self, monkeypatch, mock_files_management):
        def mock_set_data(*args, **kwargs):
            raise FileNotFoundError

        monkeypatch.setattr(FilesManagement, '_set_data', mock_set_data)

    # tests
    def test_get_logs_client(self, mock_files_management_set_data):
        return_value = self.get_logs('client')
        expected_value = {'logs': ['log1', 'log2', 'log3']}
        assert return_value.json == expected_value

    def test_get_logs_service(self, mock_files_management_set_data):
        return_value = self.get_logs('service')
        expected_value = {'logs': ['log1', 'log2', 'log3']}
        assert return_value.json == expected_value

    def test_get_logs_incorrect_name(self, mock_files_management_set_data):
        return_value = self.get_logs('incorrect_name')
        expected_value = {'message': 'Incorrect name. Expected: "client", "service"'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 422

    def test_get_logs_file_not_found(self, mock_files_management_file_not_found):
        return_value = self.get_logs('service')
        expected_value = {'message': 'File does not exist.'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 404

    def test_delete(self, mock_files_management_set_data):
        return_value = self.delete_logs('client', timestamp='2022-10-10 12:00:00')
        expected_value = {'message': 'Logs deleted successfully.'}
        assert return_value.json == expected_value

    def test_delete_logs_no_value(self, mock_files_management_set_data):
        return_value = self.delete_logs('client')
        expected_value = {'message': 'No value. Expected value for key: \'timestamp\''}
        assert return_value[0].json == expected_value
        assert return_value[1] == 400

    def test_delete_logs_wrong_date_format(self, mock_files_management_set_data):
        return_value = self.delete_logs('client', timestamp='WrongDateFormat')
        expected_value = {'message': 'Wrong date format. Expected: "%Y-%m-%d %H:%M:%S.%f"'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 422

    def test_delete_logs_incorrect_name(self, mock_files_management_set_data):
        return_value = self.delete_logs('incorrect_name')
        expected_value = {'message': 'Incorrect name. Expected: "client", "service"'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 422

    def test_delete_logs_file_not_found(self, mock_files_management_file_not_found):
        return_value = self.get_logs('client')
        expected_value = {'message': 'File does not exist.'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 404
