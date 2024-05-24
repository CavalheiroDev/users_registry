from chalice import Chalice
from chalicelib import settings

app = Chalice(
    app_name='users_registry',
    debug=settings.DEBUG
)
app.log.setLevel(settings.LOG_LEVEL)


@app.route('/healthcheck', methods=['GET'], content_types=['application/json'])
def index():
    return {'app_version': settings.APP_VERSION, 'debug': settings.DEBUG}
