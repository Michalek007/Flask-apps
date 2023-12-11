import pytest
from flask import current_app

from request_context import RequestContext
from app.blueprints.auth.views import login


class TestAuth:
    # requests
    def login(self, **kwargs):
        return RequestContext.request('/login/', login, query_string=kwargs, method='POST')

    # private fixtures
    # tests
    def test_login_no_values(self):
        return_value = self.login()
        expected_value = {'message': 'No value. Expected values for keys: \'login\', \'password\''}
        assert return_value[0].json == expected_value
        assert return_value[1] == 400
