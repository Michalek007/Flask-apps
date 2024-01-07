
class ServiceMethods:
    """ Util class for service methods. """
    @staticmethod
    def get():
        """ Returns all service methods which are meant to use by user. """
        from app.blueprints.auth.views import login
        from app.blueprints.user.views import register, logout, protected, users
        from app.blueprints.details.views import app_details
        from app.blueprints.params.views import performance, params, add_params, delete_params, update_params
        return [
            login,
            logout,
            protected,
            register,
            users,
            performance,
            app_details,
            params,
            add_params,
            delete_params,
            update_params
        ]
