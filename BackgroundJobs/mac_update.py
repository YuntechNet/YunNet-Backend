import asyncio
from datetime import datetime, timedelta
from Base import SQLPool, aiohttpSession
from aiomysql.cursors import DictCursor
from aiohttp.web_response import Response


class mac_update_status:
    running: bool = False
    last_run: datetime = None


async def mac_update(api_endpoint: str):
    while True:
        if mac_update_status.last_run is not None:
            # update already run
            last_run = datetime.now()
            await do_mac_update(api_endpoint)
            # calculate next run delay
            nextrun = datetime.now()
            nextrun = nextrun.replace(
                hour=nextrun.hour + 1, minute=0, second=0, microsecond=0
            )
            delta: timedelta = nextrun - last_run
            # sleep
            await asyncio.sleep(delta.total_seconds())
        else:
            # backend just started, do update now
            last_run = datetime.now()
            await do_mac_update(api_endpoint)
            # calculate next run delay
            nextrun = datetime.now()
            nextrun = nextrun.replace(
                hour=nextrun.hour + 1, minute=0, second=0, microsecond=0
            )
            delta: timedelta = nextrun - last_run
            if delta.total_seconds() < 60 * 10:  # 10 min
                # add another hour
                nextrun = nextrun.replace(
                    hour=nextrun.hour + 1, minute=0, second=0, microsecond=0
                )
            await asyncio.sleep(delta.total_seconds())


async def do_mac_update(api_endpoint: str):
    if mac_update_status.running is True:
        return
    mac_update_status.running = True
    try:
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                cur: DictCursor = cur
                cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify'"
                )
                mac_verify = cur.fetchone()["value"]
                cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify_changed'"
                )
                mac_verify_changed = cur.fetchone()["value"]
                cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify'"
                )
                source_verify = cur.fetchone()["value"]
                cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify_changed'"
                )
                source_verify_changed = cur.fetchone()["value"]
                ip_query = "SELECT `ip`,`switch_id`,`port`,`port_type`  FROM `ip` WHERE `is_updated` = 0"
                cur.execute(ip_query)
                ip = cur.fetchall()
                switch_query = "SELECT `switch_id`, `upper_id`, `upper_port`, `upper_port_type`, `account`, `password`, `vlan`, `machine_type`, `port_description`, `port_type` FROM `switch`"
                cur.execute(switch_query)
                switch = cur.fetchall()
                payload = {
                    "mac_verify": mac_verify,
                    "mac_verify_changed": mac_verify_changed,
                    "source_verify": source_verify,
                    "source_verify_changed": source_verify_changed,
                    "ip": ip,
                    "switch": switch,
                }
                async with aiohttpSession.session.post(
                    api_endpoint, json=payload
                ) as resp:
                    resp: Response = resp
                    if resp.status == 200:
                        update_query = (
                            "UPDATE `ip` SET `is_updated` = '1' WHERE `updated` = '0'"
                        )
                        cur.execute(update_query)
                        cur.execute(
                            "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'mac_verify_changed'"
                        )
                        cur.execute(
                            "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'source_verify_changed'"
                        )
    except Exception as e:
        mac_update_status.running = False
        raise e
