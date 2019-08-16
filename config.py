"""
Configuration file for YunNet-Backend
"""
import sanic

# ---Begin configuration file--- #


"""
Sanic debug mode
"""
DEBUG = True
DEBUG_ENABLE_SMTP = False
DEBUG_ENABLE_SQL = False
DEBUG_PRINT_SQL_ONLY = False
DEBUG_ENABLE_MONGO = False

"""
Logger SocketHandler configuration
"""
LOGGING_SOCKET_ENABLED = False
LOGGING_SOCKET = {"host": "logger", "port": 9000}


"""
Password salt
"""

PASSWORD_SALT = "PutYourSuperLongSaltSecretHereForPasswordHash"

"""
JWT secret
"""
JWT = {
    "useRSA": False,  # RSA support is at low priority
    "jwtSecret": "PutYourLongJsonWebTokenSecretHereForVerifyingSignature",
    "algorithm": "HS256",  # set approriate algorithm
    # 'jwtPublicKey': '',
    # 'jwtPrivateKey': '',
}

"""
SMTP Client parameters
"""
SMTP_CLIENT_PARAMETERS = {"hostname": "", "port": 465, "use_tls": True}
SMTP_CREDENTIALS = {"username": "", "password": ""}

"""
SQL_CREDENTIALS is the parameters of Connection constructor in PyMySQL
https://pymysql.readthedocs.io/en/latest/modules/connections.html#pymysql.connections.Connection
"""
SQL_CREDENTIALS = {
    "host": "db",
    "port": 3306,
    "user": "",
    "password": "",
    "db": "YunNet",
    "autocommit": True,
}

"""
Setup MongoDB for logging
"""
MONGODB_URI = "mongodb://mongo:27017"

"""
Google reCaptcha configuration
"""
RECAPTCHA = {"enabled": True, "secret": ""}

"""
Sanic app configuration
https://sanic.readthedocs.io/en/latest/sanic/deploying.html
"""
SANIC_APP: dict = {
    "host": "0.0.0.0",
    "port": "8000",
    # 'debug': False,
    "ssl": None,
    # 'sock': None,
    # 'workers': 1,
    # 'loop': None,
    # 'protocol': sanic.websocket.HttpProtocol,
    # 'access_log': True,
}

"""
Sanic configuration
Uncomment if you want to modify it
https://sanic.readthedocs.io/en/latest/sanic/config.html
"""
# REQUEST_MAX_SIZE = 100000000
# REQUEST_BUFFER_QUEUE_SIZE = 100
# REQUEST_TIMEOUT = 60
# RESPONSE_TIMEOUT = 60
# KEEP_ALIVE = True
# KEEP_ALIVE_TIMEOUT = 5
# GRACEFUL_SHUTDOWN_TIMEOUT = 15.0
# ACCESS_LOG = True
# PROXIES_COUNT = -1
# FORWARDED_FOR_HEADER = "X-Forwarded-For"
# REAL_IP_HEADER = "X-Real-IP"
