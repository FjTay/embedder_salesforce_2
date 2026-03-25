import os

import dotenv
import simple_salesforce

import contexts.loader


def _get_salesforce_client():
    dotenv.load_dotenv()
    return simple_salesforce.Salesforce(
        username=os.getenv("SF_USERNAME"),
        password=os.getenv("SF_PASSWORD"),
        security_token=os.getenv("SF_SECURITY_TOKEN"),
        domain=os.getenv("SF_LOGIN_DOMAIN", "login"),
    )


def load_salesforce_contexts():
    base_contexts = contexts.loader.load_contexts()
    client = _get_salesforce_client()
    org_desc = client.describe()
    sobjects = org_desc.get("sobjects", [])
    labels = {}
    for s in sobjects:
        name = s.get("name")
        if name:
            labels[name] = s.get("label") or s.get("labelPlural") or name

    result = {}
    for name, local_text in base_contexts.items():
        label = labels.get(name, "")
        if label:
            result[name] = f"{name} ({label}): {local_text}"
        else:
            result[name] = local_text
    return result
