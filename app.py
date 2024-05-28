from chalice import Chalice
from chalice.app import Request, Response
from chalicelib import settings
from chalicelib.exceptions.validation_error import ChaliceValidationError
from chalicelib.views.user_views import user_router

app = Chalice(
    app_name='users_registry',
    debug=settings.DEBUG
)
app.log.setLevel(settings.LOG_LEVEL)
app.register_blueprint(user_router, url_prefix='/users')


@app.middleware('http')
def handle_validation_error_middleware(event: Request, get_response):
    try:
        return get_response(event)
    except ChaliceValidationError as error:
        return Response(body=error.messages, status_code=error.status_code)


@app.route('/healthcheck', methods=['GET'], content_types=['application/json'])
def healthcheck():
    return {'app_version': settings.APP_VERSION, 'debug': settings.DEBUG}
