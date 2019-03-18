from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import NotFound, MethodNotSupported

from api import api


def create_app():
    app = Sanic('YunNet-Backend')
    
    
    
    @app.route('favicon.ico')
    def app_favicon(request):
        return text('')
    @app.exception(NotFound)
    def app_notfound(request, exception):
        return json({'message': 'Invalid endpoint.'}, status=404)
    @app.exception(MethodNotSupported)
    def app_method_not_supported(request, exception):
        return json({'message': 'Method not supported'}, status=405)
    app.blueprint(api)
    return app


if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
