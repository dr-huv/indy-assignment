import json
from indy import  wallet
from indy.error import  WalletAlreadyExistsError

async def create_arjun_wallet():
    try:
        arjun_wallet_config = json.dumps({"id": "arjun_wallet"})
        arjun_wallet_credentials = json.dumps({"key": "arjun_wallet_key"})
        
        try:
            await wallet.create_wallet(arjun_wallet_config, arjun_wallet_credentials)
            print("Arjun's wallet created successfully.")
        except WalletAlreadyExistsError:
            print("Arjun's wallet already exists. Skipping creation.")
        
        arjun_wallet = await wallet.open_wallet(arjun_wallet_config, arjun_wallet_credentials)
        print("Arjun's wallet opened successfully.")
        return arjun_wallet
    except Exception as e:
        print(f"Error creating Arjun's wallet: {e}")
        raise