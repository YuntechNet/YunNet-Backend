from bson import ObjectId

from Base import MongoDB
from .utils import _process_result

async def log_mac_change(ip, owner, old_mac, new_mac):
    log_entry = {
        "ip": ip,
        "owner": owner,
        "old_mac": old_mac,
        "new_mac": new_mac,
        }
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["mac_change"]
    await log_collection.insert_one(log_entry)

async def query_mac_change_by_ip(ip, skip=0, length=100):
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["mac_change"]
    cursor = log_collection.find({"ip": ip}, skip=skip, sort=[("_id", -1)])
    result = await cursor.to_list(length=length)
    return _process_result(result)

async def query_mac_change_by_owner(owner, skip=0, length=100):
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["mac_change"]
    cursor = log_collection.find({"owner": owner}, skip=skip, sort=[("_id", -1)])
    result = await cursor.to_list(length=length)
    return _process_result(result)
