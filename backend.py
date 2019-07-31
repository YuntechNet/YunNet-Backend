from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from types import SimpleNamespace
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



@app.listener('before_server_start')
async def init(app, loop):
    """
    Initializes aiohttp session for global use  
    Refers to note at: 
    https://aiohttp.readthedocs.io/en/stable/client_quickstart.html#make-a-request
    """
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)
    app.mongo = SimpleNamespace()
    app.mongo.motor_client = AsyncIOMotorClient(config.MONGODB_URI)
    app.mongo.log_db: AsyncIOMotorDatabase = app.mongo.motor_client['yunnet']
    app.mongo.log_collection: AsyncIOMotorCollection = app.mongo.log_db['log']



@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.aiohttp_session.close())
    loop.close()


@app.middleware('response')
async def response_middleware(request, response):
    response.headers["X-XSS-Protection"] = "1; mode=block"
    real_ip: str
    if 'X-Forwarded-For' in request.headers:
        real_ip = request.headers['X-Forwarded-For']
    else:
        real_ip = request.ip
    log_entry = {
        "method": request.method,
        "ip": real_ip,
        "endpoint": request.path,
        "query_string": request.query_string,
    }
    log_collection = request.app.mongo.log_collection
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
