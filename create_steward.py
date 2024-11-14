import json
from indy import  wallet,did
from indy.error import  WalletAlreadyExistsError

async def create_steward():
    steward_wallet_config = json.dumps({"id": "steward_wallet"})
    steward_wallet_credentials = json.dumps({"key": "steward_wallet_key"})
    
    try:
        await wallet.create_wallet(steward_wallet_config, steward_wallet_credentials)
        print("Steward wallet created successfully.")
    except WalletAlreadyExistsError:
        print("Steward wallet already exists. Skipping wallet creation.")
    
    steward_wallet = await wallet.open_wallet(steward_wallet_config, steward_wallet_credentials)
    
    steward_did, steward_verkey = await did.create_and_store_my_did(steward_wallet, "{}")
    print(f"Steward DID: {steward_did}, Verkey: {steward_verkey}")
    return steward_wallet, steward_did, steward_verkey