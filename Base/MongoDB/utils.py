from bson import ObjectId

def _process_result(result):
    ret = result
    for entry in ret:
        oid: ObjectId = entry.pop("_id")
        entry["id"] = str(oid)
        generation_time_utc = oid.generation_time
        generation_time = generation_time_utc.astimezone(tz=None)
        entry["date"] = generation_time.strftime("%Y-%m-%d %H:%M:%S")
    return ret
