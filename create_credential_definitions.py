import json
from indy import anoncreds, ledger

async def create_credential_definitions(pool_handle, steward_wallet, steward_did, 
                                         academic_schema_id, academic_schema_json, 
                                         research_schema_id, research_schema_json):
    try:
        print(f"\nDebug - Academic Schema ID: {academic_schema_id}")
        print(f"Debug - Academic Schema JSON: {academic_schema_json}")
        
        # Validate schema format
        academic_schema_dict = json.loads(academic_schema_json)
        if 'seqNo' not in academic_schema_dict:
            # Get schema from ledger to get seqNo
            get_schema_request = await ledger.build_get_schema_request(steward_did, academic_schema_id)
            get_schema_response = await ledger.submit_request(pool_handle, get_schema_request)
            _, retrieved_schema = await ledger.parse_get_schema_response(get_schema_response)
            academic_schema_json = retrieved_schema
            print(f"Debug - Retrieved Academic Schema: {retrieved_schema}")

        # Create Academic Credential Definition
        academic_cred_def_tag = 'TAG1'
        academic_cred_def_type = 'CL'
        academic_cred_def_config = json.dumps({"support_revocation": False})

        print("\nCreating Academic Credential Definition...")
        (academic_cred_def_id, academic_cred_def_json) = \
            await anoncreds.issuer_create_and_store_credential_def(
                steward_wallet,
                steward_did,
                academic_schema_json,
                academic_cred_def_tag,
                academic_cred_def_type,
                academic_cred_def_config
            )
        
        print(f"Debug - Academic Cred Def ID: {academic_cred_def_id}")
        print(f"Debug - Academic Cred Def JSON: {academic_cred_def_json}")

        # Validate Research Schema similarly
        print(f"\nDebug - Research Schema ID: {research_schema_id}")
        print(f"Debug - Research Schema JSON: {research_schema_json}")
        
        research_schema_dict = json.loads(research_schema_json)
        if 'seqNo' not in research_schema_dict:
            get_schema_request = await ledger.build_get_schema_request(steward_did, research_schema_id)
            get_schema_response = await ledger.submit_request(pool_handle, get_schema_request)
            _, retrieved_schema = await ledger.parse_get_schema_response(get_schema_response)
            research_schema_json = retrieved_schema
            print(f"Debug - Retrieved Research Schema: {retrieved_schema}")

        # Create Research Credential Definition
        research_cred_def_tag = 'TAG1'
        research_cred_def_type = 'CL'
        research_cred_def_config = json.dumps({"support_revocation": False})

        print("\nCreating Research Credential Definition...")
        (research_cred_def_id, research_cred_def_json) = \
            await anoncreds.issuer_create_and_store_credential_def(
                steward_wallet,
                steward_did,
                research_schema_json,
                research_cred_def_tag,
                research_cred_def_type,
                research_cred_def_config
            )

        print(f"Debug - Research Cred Def ID: {research_cred_def_id}")
        print(f"Debug - Research Cred Def JSON: {research_cred_def_json}")

        # Submit credential definitions to ledger
        print("\nSubmitting Academic Credential Definition to ledger...")
        academic_cred_def_request = await ledger.build_cred_def_request(
            steward_did, 
            academic_cred_def_json
        )
        await ledger.sign_and_submit_request(
            pool_handle, 
            steward_wallet, 
            steward_did, 
            academic_cred_def_request
        )

        print("\nSubmitting Research Credential Definition to ledger...")
        research_cred_def_request = await ledger.build_cred_def_request(
            steward_did, 
            research_cred_def_json
        )
        await ledger.sign_and_submit_request(
            pool_handle, 
            steward_wallet, 
            steward_did, 
            research_cred_def_request
        )

        print(f"\nSuccessfully created and submitted Credential Definitions")
        print(f"Academic Credential Definition ID: {academic_cred_def_id}")
        print(f"Research Credential Definition ID: {research_cred_def_id}")

        # Verify credential definitions are on the ledger
        print("\nVerifying credential definitions on ledger...")

        # Verify Academic Credential Definition
        get_academic_cred_def_request = await ledger.build_get_cred_def_request(
            steward_did, 
            academic_cred_def_id
        )
        get_academic_cred_def_response = await ledger.submit_request(
            pool_handle,
            get_academic_cred_def_request
        )
        print(f"Debug - Academic Cred Def Response: {get_academic_cred_def_response}")

        # Verify Research Credential Definition
        get_research_cred_def_request = await ledger.build_get_cred_def_request(
            steward_did, 
            research_cred_def_id
        )
        get_research_cred_def_response = await ledger.submit_request(
            pool_handle,
            get_research_cred_def_request
        )
        print(f"Debug - Research Cred Def Response: {get_research_cred_def_response}")

        return academic_cred_def_id, research_cred_def_id

    except Exception as e:
        print(f"Error in create_credential_definitions: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")  # Include detailed traceback
        raise
