import asyncio
from sanic.log import logger
from datetime import datetime, timedelta
import json
from email.mime.text import MIMEText
from aiomysql.cursors import DictCursor
from aiohttp.client import ClientResponse
from Base import big5_encode
from Base import SQLPool, aiohttpSession, SMTP

class switch_update_status:
    lock = asyncio.Lock()
    last_run: datetime = None


async def switch_update(api_endpoint: str):
    while True:
        if switch_update_status.last_run is not None:
            # update already run
            last_run = datetime.now()
            await do_switch_update(api_endpoint)
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
            await do_switch_update(api_endpoint)
            # calculate next run delay
            nextrun = datetime.now()
            nextrun = nextrun.replace(
                hour=nextrun.hour + 1, minute=10, second=0, microsecond=0
            )
            delta: timedelta = nextrun - last_run
            if delta.total_seconds() < 60 * 10:  # 10 min
                # add another hour
                nextrun = nextrun.replace(
                    hour=nextrun.hour + 1, minute=10, second=0, microsecond=0
                )
            await asyncio.sleep(delta.total_seconds())


async def do_switch_update(api_endpoint: str, forced: bool=False):
    if switch_update_status.lock.locked() and not forced:
        return
    now = datetime.now()
    async with switch_update_status.lock:
        # check if service is alive
        try:
            pass # heartbeat is pretty unnecessary 
            #await aiohttpSession.session.get(api_endpoint + "/heartbeat")
            #await asyncio.sleep(60 * 10) # wait 10 monutes
        except Exception as e:
            logger.error("[YunNet.SwitchUpdate] Can't contact to switch!")
            logger.exception(e)
            return
    
        logger.info("[YunNet.SwitchUpdate] Updating switch...")
        async with SQLPool.acquire() as conn:
            #panda step 1, grab all panda IP
            panda_ip_list = []
            async with conn.cursor() as cur:
                panda_ip_query = "SELECT `ip` from `iptable` WHERE `ip_type_id` = '2'"
                await cur.execute(panda_ip_query)
                panda_ip_list = await cur.fetchall()
            async with conn.cursor(DictCursor) as cur:
                # panda step 2, set panda IP not update on 0AM and 7AM
                panda_locked = False
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'panda_activated'"
                )
                panda_activated = (await cur.fetchone())["value"]
                if (now.hour < 7 and not panda_activated) or (now.hour >= 7 and panda_activated): 
                    # we should activate panda now
                    if now.hour < 7:
                        panda_locked = True
                        await cur.execute(
                                "UPDATE `variable` SET `value` = '1' WHERE `variable`.`name` = 'panda_activated'"
                        )
                    else:
                        panda_locked = False
                        await cur.execute(
                                "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'panda_activated'"
                        )
                    panda_lock_query = "UPDATE `iptable` SET `is_updated` = '0' WHERE `ip_type_id` = '2'"
                    await cur.execute(panda_lock_query)
                # grab variables
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'switch_update_enabled'"
                )
                switch_update_enabled = (await cur.fetchone())["value"]
                switch_update_enabled = bool(int(switch_update_enabled))
                if not switch_update_enabled:
                    logger.info("[YunNet.SwitchUpdate] Switch update is disabled!")
                    return
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify'"
                )
                mac_verify = (await cur.fetchone())["value"]
                mac_verify = bool(int(mac_verify))
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify_changed'"
                )
                mac_verify_changed = (await cur.fetchone())["value"]
                mac_verify_changed = bool(int(mac_verify_changed))
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify'"
                )
                source_verify = (await cur.fetchone())["value"]
                source_verify = bool(int(source_verify))
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify_changed'"
                )
                source_verify_changed = (await cur.fetchone())["value"]
                source_verify_changed = bool(int(source_verify_changed))
                # grab IP
                ip_query = "SELECT `ip`,`switch_id`,`port`,`port_type`,`lock_id`,`mac`  FROM `iptable` WHERE `is_updated` = 0 AND `ip_type_id` != 0"
                if mac_verify_changed or source_verify_changed:
                    ip_query = "SELECT `ip`,`switch_id`,`port`,`port_type`,`lock_id`,`mac`  FROM `iptable` WHERE `ip_type_id` != 0"
                await cur.execute(ip_query)
                ip = await cur.fetchall()
                for entry in ip:
                    if entry["lock_id"] is None:
                        entry["lock"] = False
                    else:
                        entry["lock"] = True
                    entry.pop("lock_id")
                # grab switches+ "/heartbeat"
                switch_query = "SELECT `ip`, `id`, `upper_switch`, `upper_port`, `upper_port_type`, `account`, `password`, `vlan`, `machine_type`, `port_description`, `port_type` FROM `switch`"
                await cur.execute(switch_query)
                switch = await cur.fetchall()
                for s in switch:
                    s["port_description"] = json.loads(s["port_description"])
                    s["port_type"] = json.loads(s["port_type"])
                # panda step 3, change panda IP to locked state
                if now.hour < 7: 
                    for entry in ip:
                        if entry["ip"] in panda_ip_list:
                            entry["lock"] = panda_locked
                # Send switch updating info to updater
                payload = {
                    "mac_verify": mac_verify,
                    "mac_verify_changed": mac_verify_changed,
                    "source_verify": source_verify,
                    "source_verify_changed": source_verify_changed,
                    "ip": ip,                        
                    "switch": switch,
                }
                http_status_code = 0
                update_failed_ip = []
                text = None
                try:
                    async with aiohttpSession.session.post(
                        api_endpoint + "/update", json=payload, timeout=None
                    ) as resp:
                        resp: ClientResponse = resp
                        http_status_code = resp.status
                        text = await resp.text()
                        json_body = await resp.json()
                        logger.info("[YunNet.SwitchUpdate] Got response {0}: {1}".format(resp.status, text))
                        if resp.status == 200 or resp.status == 202:
                            update_query = (
                                "UPDATE `iptable` SET `is_updated` = '1' WHERE `is_updated` = '0'"
                            )
                            await cur.execute(update_query)

                        if resp.status == 200:
                            await cur.execute(
                                "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'mac_verify_changed'"
                            )
                            await cur.execute(
                                "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'source_verify_changed'"
                            )
                        if resp.status == 202:
                            update_failed_ip = json_body["update_failed_ip"]
                            update_failed_query = (
                                "UPDATE `iptable` SET `is_updated` = '0' WHERE `ip` = %s"
                            )
                            await cur.executemany(update_failed_query, update_failed_ip)
                except e:
                    import traceback
                    text = traceback.format_exc()
                #send report
                subject = "[YunNet.SwitchUpdate] "
                message = MIMEText(text, _charset="big5")
                if http_status_code == 200:
                    subject += "Updated sucessfully."
                elif http_status_code == 202:
                    subject += "Updated with error."
                    message = MIMEText(payload, _charset="big5")
                else:
                    subject += "Failed to update."
                    message = MIMEText(payload, _charset="big5")
                if SMTP.initialized:
                    message["From"] = SMTP.sender
                    message["To"] = SMTP.sender
                    message["Subject"] = subject
                    await SMTP.send_message(message)
