import pytest
import win32api
import psutil
import datetime

from request_context import RequestContext
from app.blueprints.user.user_class import UserClass


class TestUser:
    # requests
    def logged_users(self):
        return RequestContext.request('/logged_users/', UserClass(), UserClass.logged_users)

    @pytest.fixture
    def mock_psutil_users(self, monkeypatch):
        class User:
            def __init__(self, name):
                self.name = name
        monkeypatch.setattr(psutil, 'users', lambda *args, **kwargs: [User('user1'), User('user2')])

    # tests
    def test_logged_users(self, mock_psutil_users):
        return_value = self.logged_users()
        expected_value = {'logged_users': ['user1', 'user2']}
        assert return_value.json == expected_value
