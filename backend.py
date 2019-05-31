from sanic import Sanic
from sanic.log import logger
from sanic.response import json, text
from sanic.exceptions import NotFound, MethodNotSupported
from argparse import ArgumentParser
import aiohttp

from api import api
from api import messages
import config

app: Sanic = Sanic('YunNet-Backend')
app.config.from_object(config)

@app.listener('before_server_start')
def init(app, loop):
    """
    Initializes aiohttp session for global use  
    Refers to note at: 
    https://aiohttp.readthedocs.io/en/stable/client_quickstart.html#make-a-request
    """
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)
@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.session.close())
    loop.close()
@app.route('favicon.ico')
async def app_favicon(request):
    return text('')
@app.exception(NotFound)
async def app_notfound(request, exception):
    return json(messages.INVALID_ENDPOINT, status=404)
@app.exception(MethodNotSupported)
async def app_method_not_supported(request, exception):
    return json(messages.METHOD_NOT_SUPPORTED, status=405)

# import API blueprints into app
app.blueprint(api)

if __name__=='__main__':
    app.run(config.SANIC_APP)
