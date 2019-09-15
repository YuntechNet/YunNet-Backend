from Base import MongoDB
from .utils import _process_result

async def log_login(username):
    log_entry = {
        "username": username,
        "action": "login"
    }
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    await log_collection.insert_one(log_entry)


async def log_register(username):
    log_entry = {
        "username": username,
        "action": "register"
    }
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    await log_collection.insert_one(log_entry)


async def log_activate(username):
    log_entry = {
        "username": username,
        "action": "activate"
    }
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    await log_collection.insert_one(log_entry)

async def log_change_password(username):
    log_entry = {
        "username": username,
        "action": "change_password"
    }
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    await log_collection.insert_one(log_entry)

async def query_actions(username, length=100):
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    cursor = log_collection.find({"username":  username})
    result = await cursor.to_list(length=length)
    return _process_result(result)