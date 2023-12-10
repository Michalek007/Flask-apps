import pytest

from request_context import RequestContext
from app.blueprints.config.config_class import ConfigClass
from configuration import Pid
from utils import SubprocessApi, ProcessUtil


class TestConfig:
    # requests
    def set_client_status(self, **kwargs):
        return RequestContext.request('/set_client_status/', ConfigClass(), ConfigClass.set_client_status, query_string=kwargs)

    def get_client_status(self):
        return RequestContext.request('/get_client_status/', ConfigClass(), ConfigClass.get_client_status)

    def get_pid(self):
        return RequestContext.request('/get_pid/', ConfigClass(), ConfigClass.get_pid)

    def set_pid(self, **kwargs):
        return RequestContext.request('/set_pid/', ConfigClass(), ConfigClass.set_pid, query_string=kwargs)

    def kill(self):
        return RequestContext.request('/kill/', ConfigClass(), ConfigClass.kill)

    def restart(self):
        return RequestContext.request('/restart/', ConfigClass(), ConfigClass.restart)

    def kill_client(self):
        return RequestContext.request('/kill_client/', ConfigClass(), ConfigClass.kill_client)

    def restart_client(self):
        return RequestContext.request('/restart_client/', ConfigClass(), ConfigClass.restart_client)

    # private fixtures
    @pytest.fixture
    def mock_process_util_find_process_false(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'find_process', lambda *args, **kwargs: False)

    @pytest.fixture
    def mock_process_util_find_process_true(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'find_process', lambda *args, **kwargs: True)

    @pytest.fixture
    def mock_process_util_task_kill(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'task_kill', lambda *args, **kwargs: None)

    @pytest.fixture
    def mock_process_util_task_kill_capture_output(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'task_kill',
                            lambda *args, **kwargs: (None, None))

    @pytest.fixture
    def mock_process_util_task_kill_capture_output_error(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'task_kill',
                            lambda *args, **kwargs: (None, ['ERROR: The process "None" not found.']))

    @pytest.fixture
    def mock_subprocess_api_run(self, monkeypatch):
        monkeypatch.setattr(SubprocessApi, 'run', lambda *args, **kwargs: None)

    # tests
    def test_set_client_status(self):
        return_value = self.set_client_status(status='Status1')
        expected_value = {'message': 'Client status set successfully.'}
        assert return_value.json == expected_value

    def test_set_client_status_no_value(self):
        return_value = self.set_client_status()
        expected_value = {'message': 'Wrong key or value was not provided. Expected key: \'status\''}
        assert return_value[0].json == expected_value
        assert return_value[1] == 400

    def test_set_pid(self):
        pid = 420
        return_value = self.set_pid(client=pid)
        expected_value = {'message': 'PID updated successfully.'}
        assert return_value.json == expected_value
        assert Pid.CLIENT == pid

    def test_set_pid_no_value(self):
        return_value = self.set_pid()
        expected_value = {'message': 'Wrong key or value was not provided. Expected key: \'client\''}
        assert return_value[0].json == expected_value
        assert return_value[1] == 400

    def test_set_pid_no_integer(self):
        return_value = self.set_pid(client='no integer')
        expected_value = {'message': 'PID must be an integer.'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 422

    def test_get_pid(self, mock_process_util_find_process_false):
        Pid.CLIENT = 420
        Pid.SERVICE = 421
        return_value = self.get_pid()
        expected_value = {'SERVICE': 421, 'CLIENT': None}
        assert return_value.json == expected_value

    def test_get_pid_none(self, mock_process_util_find_process_true):
        Pid.CLIENT = 420
        Pid.SERVICE = 421
        return_value = self.get_pid()
        expected_value = {'SERVICE': 421, 'CLIENT': 420}
        assert return_value.json == expected_value

    def test_kill(self, mock_process_util_task_kill):
        return_value = self.kill()
        expected_value = {'message': 'Service is shut down!'}
        assert return_value.json == expected_value

    def test_restart(self, mock_process_util_task_kill, mock_subprocess_api_run):
        return_value = self.restart()
        expected_value = {'message': 'Service is restarting!'}
        assert return_value.json == expected_value

    def test_kill_client(self, mock_process_util_task_kill_capture_output):
        return_value = self.kill_client()
        expected_value = {'message': 'Client is shut down!'}
        assert return_value.json == expected_value

    def test_kill_client_no_pid(self, mock_process_util_task_kill_capture_output_error):
        return_value = self.kill_client()
        expected_value = {'message': 'ERROR: The process "None" not found.'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 404

    def test_restart_client(self, mock_process_util_task_kill, mock_subprocess_api_run):
        return_value = self.restart_client()
        expected_value = {'message': 'Client is restarting!'}
        assert return_value.json == expected_value
