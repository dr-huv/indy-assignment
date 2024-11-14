from indy.error import PoolLedgerConfigAlreadyExistsError, PoolLedgerTimeout
import json
from indy import pool

async def connect_to_pool():
    pool_name = 'pool1'
    pool_config = json.dumps({"genesis_txn": "pool1.txn"})
    
    try:
        await pool.create_pool_ledger_config(pool_name, pool_config)
        print("Pool ledger config created.")
    except PoolLedgerConfigAlreadyExistsError:
        print("Pool ledger config already exists. Skipping creation.")
    
    print(f"Attempting to open the pool: {pool_name}")

    try:
        pool_handle = await pool.open_pool_ledger(pool_name, None)
        print("Pool connected successfully.")
        return pool_handle
    except PoolLedgerTimeout as e:
        print(f"Error: Pool ledger connection timed out. {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while opening pool: {e}")
        raise