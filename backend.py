import asyncio
from BackgroundJobs import mac_update
from Base import aiohttpSession, SMTP, SQLPool, messages
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
import datetime
from email.mime.text import MIMEText
import time
import jwt
import logging
import traceback
from types import SimpleNamespace
from sanic import Sanic
from sanic.log import error_logger
from sanic.request import Request
from sanic.response import json, text, redirect
from sanic.exceptions import NotFound, MethodNotSupported
from argparse import ArgumentParser

import aiohttp

from sanic_openapi import swagger_blueprint

from api import api

# from api import messages
import config

app: Sanic = Sanic("YunNet-Backend")
app.config.from_object(config)


@app.listener("before_server_start")
async def init(app, loop):
    """
    Initializes aiohttp session for global use  
    Refers to note at: 
    https://aiohttp.readthedocs.io/en/stable/client_quickstart.html#make-a-request
    """
    if config.LOGGING_SOCKET_ENABLED:
        sh = logging.handlers.SocketHandler(**config.LOGGING_SOCKET)
        error_logger.addHandler(sh)
    try:
        # init aiohttp session
        app.aiohttp_session = aiohttp.ClientSession(loop=loop)
        await aiohttpSession.init({"limit": 200})
        # init SMTP client
        if config.DEBUG_ENABLE_SMTP or (not config.DEBUG):
            print("Initializing SMTP...")
            await SMTP.init(config.SMTP_CLIENT_PARAMETERS, config.SMTP_CREDENTIALS)
        # init mongo log
        if config.DEBUG_ENABLE_MONGO or not config.DEBUG:
            print("Initializing MongoDB...")
            app.mongo = SimpleNamespace()
            app.mongo.motor_client = AsyncIOMotorClient(config.MONGODB_URI)
            app.mongo.log_db = app.mongo.motor_client["yunnet"]
            app.mongo.log_collection = app.mongo.log_db["log"]
        # init aiomysql pool
        if config.DEBUG_ENABLE_SQL or not config.DEBUG:
            print("Initializing aiomysql...")
            await SQLPool.init_pool(**config.SQL_CREDENTIALS)
        # MAC updating task
        loop.create_task(mac_update())
        raise Exception
    except Exception as ex:
        error_logger.critical(traceback.format_exc())
        raise ex


@app.listener("after_server_stop")
async def finish(app, loop):
    await app.aiohttp_session.close()
    await aiohttpSession.close()
    if config.DEBUG_ENABLE_SQL or not config.DEBUG:
        SQLPool.pool.close()
        await SQLPool.pool.wait_closed()


@app.middleware("response")
async def response_middleware(request, response):
    response.headers["X-XSS-Protection"] = "1; mode=block"
    real_ip: str = None
    username: str = None
    if "X-Forwarded-For" in request.headers:
        real_ip = request.headers["X-Forwarded-For"]
    else:
        real_ip = request.ip
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"].split()
        if auth[0] == "Bearer":
            try:
                jwt_payload = jwt.decode(auth[1], config.JWT["jwtSecret"])
                username = jwt_payload["username"]
            except:
                pass
    timenow = datetime.datetime.now()
    log_entry = {
        "timestamp": timenow,
        "unix_time": time.mktime(timenow.timetuple()),
        "method": request.method,
        "ip": real_ip,
        "username": username,
        "endpoint": request.path,
        "query_string": request.query_string,
        "http_status": response.status,
    }
    if config.DEBUG_ENABLE_MONGO or not config.DEBUG:
        log_collection = request.app.mongo.log_collection
        await log_collection.insert_one(log_entry)


@app.route("favicon.ico")
async def app_favicon(request):
    return text("")


@app.exception(NotFound)
async def app_notfound(request, ex):
    return messages.INVALID_ENDPOINT


@app.exception(MethodNotSupported)
async def app_method_not_supported(request, ex):
    return messages.METHOD_NOT_SUPPORTED


@app.exception(Exception)
async def app_other_error(request, ex):
    traceback.print_exc()
    error_logger.critical(traceback.format_exc())
    if SMTP.client is not None:
        message = MIMEText(traceback.format_exc())
        message["From"] = config.SMTP_CREDENTIALS["username"]
        message["To"] = config.SMTP_CREDENTIALS["username"]
        message["Subject"] = "[YunNet] Encountered exception."
        await SMTP.client.send_message(message)
    return messages.INTERNAL_SERVER_ERROR


# swagger api setup
app.blueprint(swagger_blueprint)

app.config.API_SECURITY = [{"authToken": []}]

app.config.API_SECURITY_DEFINITIONS = {
    "authToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": 'Paste your auth token and do not forget to add "Bearer " in front of it',
    }
}

# import API blueprints into app
app.blueprint(api)

if __name__ == "__main__":
    app.run(**config.SANIC_APP)
