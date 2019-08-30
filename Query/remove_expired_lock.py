from Base import SQLPool

async def remove_expired_lock():
    async with SQLPool.acquire() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE iptable INNER JOIN `lock` ON iptable.lock_id = `lock`.lock_id SET `iptable`.`lock_id` = NULL WHERE `unlock_date` < CURRENT_TIMESTAMP;"
            await cur.execute(sql)
            await conn.commit()
