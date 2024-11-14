import json
from indy import anoncreds, ledger

async def create_schema(pool_handle, steward_wallet, steward_did):
    try:
        academic_schema = {
            'name': 'AcademicQualification',
            'version': '1.5',
            'attributes': ['student_first_name', 'student_last_name', 'degree', 'field_of_study', 
                         'university_name', 'graduation_year', 'cgpa']
        }
        
        research_schema = {
            'name': 'ResearchAuthorship',
            'version': '1.5',
            'attributes': ['author_first_name', 'author_last_name', 'research_title', 
                         'institute_name', 'research_field', 'publication_year']
        }

        academic_schema_id, academic_schema_json = await anoncreds.issuer_create_schema(
            steward_did,
            academic_schema['name'],
            academic_schema['version'],
            json.dumps(academic_schema['attributes'])
        )

        research_schema_id, research_schema_json = await anoncreds.issuer_create_schema(
            steward_did,
            research_schema['name'],
            research_schema['version'],
            json.dumps(research_schema['attributes'])
        )

        print(f"Created Academic Schema with ID: {academic_schema_id}")
        print(f"Created Research Schema with ID: {research_schema_id}")

        academic_schema_request = await ledger.build_schema_request(steward_did, academic_schema_json)
        research_schema_request = await ledger.build_schema_request(steward_did, research_schema_json)

        await ledger.sign_and_submit_request(pool_handle, steward_wallet, steward_did, academic_schema_request)
        await ledger.sign_and_submit_request(pool_handle, steward_wallet, steward_did, research_schema_request)

        print("Schemas submitted to ledger successfully")
        return academic_schema_id, research_schema_id, academic_schema_json, research_schema_json

    except Exception as e:
        print(f"Error in create_schema: {e}")
        raise
