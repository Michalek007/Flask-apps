import pytest
import psutil

from request_context import RequestContext
from app.blueprints.hardware.hardware_class import HardwareClass


class TestsHardware:
    # requests
    def performance(self):
        return RequestContext.request('/performance/', HardwareClass(), HardwareClass.performance)

    # private fixtures
    @pytest.fixture
    def mock_psutil(self, monkeypatch):
        monkeypatch.setattr(psutil, 'cpu_percent', lambda *args, **kwargs: 50)
        monkeypatch.setattr(psutil, 'cpu_freq', lambda *args, **kwargs: [2100])
        monkeypatch.setattr(psutil, 'disk_usage', lambda *args, **kwargs: [500*10**9, 350*10**9, 150*10**9, 30])
        monkeypatch.setattr(psutil, 'virtual_memory', lambda *args, **kwargs: [32*10**9, 16*10**9, 50, 16*10**9])

    # tests
    def test_performance(self, mock_psutil):
        return_value = self.performance()
        expected_value = dict(cpu={'usage': 50, 'freq': 2100},
                              disk={'usage': 30, 'total': 500, 'used': 350, 'free': 150},
                              virtual_memory={'usage': 50, 'total': 32, 'available': 16, 'used': 16})
        assert return_value.json == expected_value
