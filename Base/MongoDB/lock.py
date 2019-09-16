from bson import ObjectId

from Base import MongoDB
from .utils import _process_result


async def log_lock(ip, current_ip_owner, operator, lock_until):
    log_entry = {
        "type": "lock",
        "ip": ip,
        "current_ip_owner": current_ip_owner,
        "operator": operator,
        "lock_until": lock_until,
        }
    # get collection
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["lock"]
    await log_collection.insert_one(log_entry)

async def log_unlock(ip, owner, operator, lock_until):
    log_entry = {
        "type": "unlock",
        "ip": ip,
        "current_ip_owner": owner,
        "operator": operator,
        "lock_until": lock_until,
        }
    # get collection
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["lock"]
    await log_collection.insert_one(log_entry)

async def query_lock_by_ip(ip, skip=0, length=100):
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    cursor = log_collection.find({"ip":  ip}, skip=skip, sort=[("_id", -1)])
    result = await cursor.to_list(length=length)
    _process_result(result)

async def query_lock_by_owner(owner, skip=0, length=100):
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["actions"]
    cursor = log_collection.find({"owner":  owner}, skip=skip, sort=[("_id", -1)])
    result = await cursor.to_list(length=length)
    _process_result(result)