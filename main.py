import asyncio
from indy import pool, wallet
from connect_to_pool import connect_to_pool
from create_steward import create_steward
from register_trust_anchors import register_trust_anchors
from create_schema import create_schema
from create_arjun_wallet import create_arjun_wallet
from create_credential_definitions import create_credential_definitions
from issue_credentials import issue_credentials
from create_and_verify_proof import create_and_verify_proof

async def main():
    try:
        pool_handle = await connect_to_pool()
        
        steward_wallet, steward_did, steward_verkey = await create_steward()
        university_did, research_institute_did = await register_trust_anchors(steward_wallet, steward_did)
        
        academic_schema_id, research_schema_id, academic_schema_json, research_schema_json = await create_schema(
            pool_handle, steward_wallet, steward_did)
        
        academic_cred_def_id, research_cred_def_id = await create_credential_definitions(
            pool_handle, steward_wallet, steward_did, 
            academic_schema_id, academic_schema_json,
            research_schema_id, research_schema_json)
        

        arjun_wallet = await create_arjun_wallet()
        

        await issue_credentials(pool_handle, steward_wallet, steward_did, arjun_wallet, 
                              academic_cred_def_id, research_cred_def_id)
        

        await create_and_verify_proof(pool_handle, arjun_wallet, academic_cred_def_id, research_cred_def_id)
        
        print("Successfully completed all operations")
        
    except Exception as e:
        print(f"Error in main: {e}")
        raise
    finally:

        if 'arjun_wallet' in locals():
            await wallet.close_wallet(arjun_wallet)
        if 'steward_wallet' in locals():
            await wallet.close_wallet(steward_wallet)
        if 'pool_handle' in locals():
            await pool.close_pool_ledger(pool_handle)

if __name__ == '__main__':
    asyncio.run(main())