import json
from indy import anoncreds

async def create_and_verify_proof(pool_handle, arjun_wallet, academic_cred_def_id, research_cred_def_id):
    try:
        proof_request = {
            'nonce': '123432421212',
            'name': 'IES Eligibility Proof',
            'version': '0.1',
            'requested_attributes': {
                'attr1_referent': {
                    'name': 'student_first_name',
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'attr2_referent': {
                    'name': 'student_last_name',
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'attr3_referent': {
                    'name': 'degree',
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'attr4_referent': {
                    'name': 'field_of_study',
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'attr5_referent': {
                    'name': 'university_name',
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'attr6_referent': {
                    'name': 'research_title',
                    'restrictions': [{'cred_def_id': research_cred_def_id}]
                },
                'attr7_referent': {
                    'name': 'research_field',
                    'restrictions': [{'cred_def_id': research_cred_def_id}]
                }
            },
            'requested_predicates': {
                'predicate1_referent': {
                    'name': 'graduation_year',
                    'p_type': '>=',
                    'p_value': 2020,
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'predicate2_referent': {
                    'name': 'graduation_year',
                    'p_type': '<=',
                    'p_value': 2023,
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'predicate3_referent': {
                    'name': 'cgpa',
                    'p_type': '>',
                    'p_value': 6,
                    'restrictions': [{'cred_def_id': academic_cred_def_id}]
                },
                'predicate4_referent': {
                    'name': 'publication_year',
                    'p_type': '>=',
                    'p_value': 2022,
                    'restrictions': [{'cred_def_id': research_cred_def_id}]
                }
            }
        }

        search_for_proof_request = await anoncreds.prover_search_credentials_for_proof_req(
            arjun_wallet, json.dumps(proof_request), None)
        credentials_for_proof = {}
        for attr in proof_request['requested_attributes']:
            credentials_for_attr = await anoncreds.prover_fetch_credentials_for_proof_req(
                search_for_proof_request, attr, 1)
            credentials_for_proof[attr] = credentials_for_attr[0]

        for pred in proof_request['requested_predicates']:
            credentials_for_pred = await anoncreds.prover_fetch_credentials_for_proof_req(
                search_for_proof_request, pred, 1)
            credentials_for_proof[pred] = credentials_for_pred[0]

        await anoncreds.prover_close_credentials_search_for_proof_req(search_for_proof_request)

        schemas = {}
        credential_defs = {}
        proof = await anoncreds.prover_create_proof(
            arjun_wallet, json.dumps(proof_request),
            json.dumps(credentials_for_proof), 
            json.dumps(schemas), json.dumps(credential_defs), "{}")

        print("Proof created successfully")
        print(json.dumps(json.loads(proof), indent=4))

    except Exception as e:
        print(f"Error in create_and_verify_proof: {e}")
        raise