from indy import did

async def register_trust_anchors(steward_wallet, steward_did):
    university_did, university_verkey = await did.create_and_store_my_did(steward_wallet, "{}")
    research_institute_did, research_institute_verkey = await did.create_and_store_my_did(steward_wallet, "{}")
    
    print(f"University DID: {university_did}")
    print(f"Research Institute DID: {research_institute_did}")
    return university_did, research_institute_did