from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from sanic import Sanic
from sanic.log import logger
from sanic.request import Request
from sanic.response import json, text, redirect
from sanic.exceptions import NotFound, MethodNotSupported
from argparse import ArgumentParser
import aiohttp

from sanic_openapi import swagger_blueprint

from api import api
# from api import messages
import config

app: Sanic = Sanic('YunNet-Backend')
app.config.from_object(config)

mongo = AsyncIOMotorClient(config.MONGODB_URI)
log_db: AsyncIOMotorDatabase = mongo['yunnet']
log_collection: AsyncIOMotorCollection = log_db['log']


@app.listener('before_server_start')
async def init(app, loop):
    """
    Initializes aiohttp session for global use  
    Refers to note at: 
    https://aiohttp.readthedocs.io/en/stable/client_quickstart.html#make-a-request
    """
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.aiohttp_session.close())
    loop.close()


@app.middleware('response')
def response_middleware(request, response):
    response.headers["X-XSS-Protection"] = "1; mode=block"
    real_ip = request.headers['X-Forwarded-For']
    log_entry = {
        "method": request.method,
        "ip": real_ip,
    }
    result = await log_collection.insert_one(log_entry)


@app.route('favicon.ico')
async def app_favicon(request):
    return text('')


@app.exception(NotFound)
async def app_notfound(request, exception):
    return json("messages.INVALID_ENDPOINT", status=404)


@app.exception(MethodNotSupported)
async def app_method_not_supported(request, exception):
    return json("messages.METHOD_NOT_SUPPORTED", status=405)


# swagger api setup
app.blueprint(swagger_blueprint)

app.config.API_SECURITY = [
    {
        'authToken': []
    }
]

app.config.API_SECURITY_DEFINITIONS = {
    'authToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Paste your auth token and do not forget to add "Bearer " in front of it'
    },
}

# import API blueprints into app
app.blueprint(api)

if __name__ == '__main__':
    app.run(**config.SANIC_APP)
