from datetime import datetime
from csv import reader

from sanic.log import logger
from hashlib import sha256
from Base import SQLPool


class BulkImportStatus:
    running: bool = False
    last_run: datetime = None


async def bulk_import(csv_string: str, password_salt):
    """
    file format as
    bed, username(student_id), nick, department,
    Args:
        filepath:

    Returns:

    """
    user_update = []
    user_create = []
    fail_list = []
    if BulkImportStatus.running is True:
        logger.error("[bulk_import] Please don't run bulk import more than 1 instance!")
        return
    else:
        BulkImportStatus.running = True
    logger.info("[bulk_import] Starting...")
    try:

        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                rows = reader(csv_string.split("\n"))
                for row in rows:
                    logger.debug("[bulk_import] Fetched: {}".format(row))

                    bed = row[0].strip().upper()
                    username = row[1].strip()
                    nick = row[2].strip()
                    department = row[3].strip().upper()

                    # TODO input validate regex

                    # check user exist
                    await cur.execute(
                        "SELECT EXISTS (SELECT * FROM user WHERE username = %s)", username
                    )
                    conn.commit()
                    is_exists = await cur.fetchall()

                    # preform user update (name,department)
                    if is_exists:
                        user_update.append((nick, department, username))
                    # user creation
                    else:
                        # TODO card id as passoword
                        encode_password = (bed + password_salt).encode("UTF-8")
                        hashed_password = sha256(encode_password).hexdigest()
                        user_create.append(
                            (None, username, hashed_password, nick, department, None, None)
                        )

                    logger.debug("[bulk_import] Processing: {}".format(row))

                logger.info("[bulk_import] Updating existing user...")
                await cur.executemany(
                    "UPDATE `user` SET `nick` = %s, `department` = %s WHERE username = %s",
                    user_update,
                )
                logger.info("[bulk_import] Inserting user...")
                await cur.executemany(
                    "INSERT INTO `user` VALUES (null,%s,%s,%s,%s,null,'')",
                    user_create,
                )
                await conn.commit()
                logger.info("[bulk_import] Finished.")
    except Exception as e:
        BulkImportStatus.running = False
        raise e


