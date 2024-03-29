from flask_login import FlaskLoginClient

from app import app


class RequestContext:
    app = app
    app.test_client_class = FlaskLoginClient

    @staticmethod
    def request(endpoint, endpoint_method, arg=None, query_string: dict = None, method='GET'):
        if arg is not None:
            endpoint = endpoint + f'/{arg}/'
        with RequestContext.app.test_request_context(
                    endpoint, query_string=query_string, method=method
        ):
            if arg is not None:
                return endpoint_method(arg)
            else:
                return endpoint_method()


### tests class schema
# import pytest
#
# from request_context import RequestContext
# from app.blueprints.bp.views import endpoint_method
# from app.blueprints.bp.modules import Module
#
#
# class TestBlueprint:
#     # requests
#     def endpoint(self, arg, **kwargs):
#         return RequestContext.request('/endpoint/', endpoint, arg=arg, query_string=kwargs)
#
#     def endpoint(self, arg):
#         return RequestContext.request('/endpoint/', endpoint, arg=arg)
#
#     def endpoint(self, **kwargs):
#         return RequestContext.request('/endpoint/', endpoint, query_string=kwargs)
#
#
#     # private fixtures
#     @pytest.fixture
#     def mock_some_class_method(self, monkeypatch):
#         monkeypatch.setattr(SomeClass, 'method', lambda *args, **kwargs: None)
#     # tests
#     def test_endpoint_condition(self, mock_some_method):
#         return_value = self.endpoint()
#         expected_value = {'message': 'Expected message'}
#         assert return_value.json == expected_value
#     def test_endpoint_other_condition(self, mock_some_method):
#         return_value = self.endpoint()
#         expected_value = {'message': 'Expected message'}
#         assert return_value[0].json == expected_value
#         assert return_value[1] == 404
