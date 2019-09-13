from bson import ObjectId

def _process_result(result):
    ret = result
    for entry in ret:
        oid: ObjectId = entry["_id"]
        entry.pop("_id")
        entry["id"] = str(oid)
        entry["date"] = oid.generation_time.strftime("%Y-%m-%d %H:%M:%S")
    return ret
