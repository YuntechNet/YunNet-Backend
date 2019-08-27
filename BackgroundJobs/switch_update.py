import asyncio
from sanic.log import logger
from datetime import datetime, timedelta
import json
from email.mime.text import MIMEText
from aiomysql.cursors import DictCursor
from aiohttp.client import ClientResponse

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
                hour=nextrun.hour + 1, minute=0, second=0, microsecond=0
            )
            delta: timedelta = nextrun - last_run
            if delta.total_seconds() < 60 * 10:  # 10 min
                # add another hour
                nextrun = nextrun.replace(
                    hour=nextrun.hour + 1, minute=0, second=0, microsecond=0
                )
            await asyncio.sleep(delta.total_seconds())


async def do_switch_update(api_endpoint: str, forced: bool=False):
    if switch_update_status.lock.locked() and not forced:
        return
    now = datetime.now()
    async with switch_update_status.lock:
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
                if now.hour == 0 or now.hour == 7: 
                    panda_lock_query = "UPDATE `iptable` SET `is_updated` = '0' WHERE `ip_type_id` = '2'"
                    await cur.execute(panda_lock_query)
                # grab variables
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify'"
                )
                mac_verify = (await cur.fetchone())["value"]
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'mac_verify_changed'"
                )
                mac_verify_changed = (await cur.fetchone())["value"]
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify'"
                )
                source_verify = (await cur.fetchone())["value"]
                await cur.execute(
                    "SELECT `value` FROM `variable` WHERE `name` = 'source_verify_changed'"
                )
                source_verify_changed = (await cur.fetchone())["value"]
                # grap IP
                ip_query = "SELECT `ip`,`switch_id`,`port`,`port_type`  FROM `iptable` WHERE `is_updated` = 0"
                if mac_verify_changed or source_verify_changed:
                    ip_query = "SELECT `ip`,`switch_id`,`port`,`port_type`  FROM `iptable`"
                await cur.execute(ip_query)
                ip = await cur.fetchall()
                # grab switches
                switch_query = "SELECT `switch_id`, `upper_id`, `upper_port`, `upper_port_type`, `account`, `password`, `vlan`, `machine_type`, `port_description`, `port_type` FROM `switch`"
                await cur.execute(switch_query)
                switch = await cur.fetchall()
                for s in switch:
                    s["port_description"] = json.loads(s["port_description"])
                    s["port_type"] = json.loads(s["port_type"])
                # panda step 3, change panda IP to locked state
                if now.hour < 7: 
                    for entry in ip:
                        if entry["ip"] in panda_ip_list:
                            entry["lock"] = True
                # Send switch updating info to updater
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
                    resp: ClientResponse = resp
                    if resp.status == 200 or resp.status == 202:
                        update_query = (
                            "UPDATE `iptable` SET `is_updated` = '1' WHERE `is_updated` = '0'"
                        )
                        await cur.execute(update_query)
                        await cur.execute(
                            "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'mac_verify_changed'"
                        )
                        await cur.execute(
                            "UPDATE `variable` SET `value` = '0' WHERE `variable`.`name` = 'source_verify_changed'"
                        )

                    update_failed_ip = []
                    if resp.status == 202:
                        update_failed_ip = resp.json()["update_failed_ip"]
                        update_failed_query = (
                            "UPDATE `iptable` SET `is_updated` = '0' WHERE `ip` = %s"
                        )
                        await cur.executemany(update_failed_query, update_failed_ip)

                    #send report
                    subject = "[YunNet.SwitchUpdate] "
                    if resp.status == 200:
                        subject += "Updated sucessfully."
                        logger.info(subject)
                    elif resp.status == 202:
                        subject += "Updated with error."
                        subject += "\n"
                        subject += update_failed_ip
                    else:
                        subject += "Failed to update."
                    logger.info(subject)
                    if SMTP.initialized:
                        message = MIMEText(update_failed_ip)
                        message["From"] = SMTP.sender
                        message["To"] = SMTP.sender
                        message["Subject"] = subject
                        SMTP.send_message(message)
