from chalice import Chalice
from chalicelib import settings
from chalicelib.views.user_views import user_router

app = Chalice(
    app_name='users_registry',
    debug=settings.DEBUG
)
app.log.setLevel(settings.LOG_LEVEL)
app.register_blueprint(user_router, url_prefix='/users')


@app.route('/healthcheck', methods=['GET'], content_types=['application/json'])
def healthcheck():
    return {'app_version': settings.APP_VERSION, 'debug': settings.DEBUG}



