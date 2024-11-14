from indy import ledger, anoncreds, did, error
import json

async def issue_credentials(pool_handle, steward_wallet, steward_did, arjun_wallet, academic_cred_def_id, research_cred_def_id):
    try:
        try:
            master_secret_id = await anoncreds.prover_create_master_secret(arjun_wallet, None)
            print("Master secret created for Arjun's wallet.")
        except error.IndyError as e:
            if e.error_code == error.ErrorCode.AnoncredsMasterSecretDuplicateNameError:
                master_secret_id = "master_secret"
                print("Using existing master secret")
            else:
                raise


        print(f"Retrieving credential definitions from ledger...")

        get_academic_cred_def_request = await ledger.build_get_cred_def_request(
            steward_did, 
            academic_cred_def_id
        )
        get_academic_cred_def_response = await ledger.submit_request(
            pool_handle,
            get_academic_cred_def_request
        )
        _, academic_cred_def_json = await ledger.parse_get_cred_def_response(
            get_academic_cred_def_response
        )

        get_research_cred_def_request = await ledger.build_get_cred_def_request(
            steward_did,
            research_cred_def_id
        )
        get_research_cred_def_response = await ledger.submit_request(
            pool_handle,
            get_research_cred_def_request
        )
        _, research_cred_def_json = await ledger.parse_get_cred_def_response(
            get_research_cred_def_response
        )

        print("Successfully retrieved credential definitions")

        academic_cred_offer = await anoncreds.issuer_create_credential_offer(
            steward_wallet,
            academic_cred_def_id
        )
        research_cred_offer = await anoncreds.issuer_create_credential_offer(
            steward_wallet,
            research_cred_def_id
        )

        (prover_did, prover_verkey) = await did.create_and_store_my_did(arjun_wallet, "{}")

        academic_cred_values = {
            "student_first_name": {"raw": "Arjun", "encoded": "1139481716457488690172217916278103335"},
            "student_last_name": {"raw": "Verma", "encoded": "5321642780241790123587902456789123452"},
            "degree": {"raw": "PhD in Environmental Science", "encoded": "12434523576212321"},
            "field_of_study": {"raw": "Sustainable Agriculture", "encoded": "12434523576212322"},
            "university_name": {"raw": "Delhi University", "encoded": "12434523576212323"},
            "graduation_year": {"raw": "2022", "encoded": "2022"},
            "cgpa": {"raw": "9", "encoded": "9"}
        }

        research_cred_values = {
            "author_first_name": {"raw": "Arjun", "encoded": "1139481716457488690172217916278103335"},
            "author_last_name": {"raw": "Verma", "encoded": "5321642780241790123587902456789123452"},
            "research_title": {"raw": "Innovative Techniques in Sustainable Farming", "encoded": "12434523576212324"},
            "institute_name": {"raw": "GreenEarth Research Institute", "encoded": "12434523576212325"},
            "research_field": {"raw": "Environmental Studies", "encoded": "12434523576212326"},
            "publication_year": {"raw": "2023", "encoded": "2023"}
        }

        print("Creating credential requests...")
        academic_cred_request, academic_cred_request_metadata = await anoncreds.prover_create_credential_req(
            arjun_wallet,
            prover_did,
            academic_cred_offer,
            academic_cred_def_json,
            master_secret_id
        )

        research_cred_request, research_cred_request_metadata = await anoncreds.prover_create_credential_req(
            arjun_wallet,
            prover_did,
            research_cred_offer,
            research_cred_def_json,
            master_secret_id
        )

        print("Issuing credentials...")
        academic_cred, _, _ = await anoncreds.issuer_create_credential(
            steward_wallet,
            academic_cred_offer,
            academic_cred_request,
            json.dumps(academic_cred_values),
            None,
            None
        )

        research_cred, _, _ = await anoncreds.issuer_create_credential(
            steward_wallet,
            research_cred_offer,
            research_cred_request,
            json.dumps(research_cred_values),
            None,
            None
        )


        print("Storing credentials in wallet...")
        await anoncreds.prover_store_credential(
            arjun_wallet,
            None,
            academic_cred_request_metadata,
            academic_cred,
            academic_cred_def_json,
            None
        )

        await anoncreds.prover_store_credential(
            arjun_wallet,
            None,
            research_cred_request_metadata,
            research_cred,
            research_cred_def_json,
            None
        )

        print("Credentials successfully issued and stored")
        return True

    except error.IndyError as e:
        print(f"Indy error occurred: {e.error_code} - {e.message}")
        raise
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise