import json


def describe_sobject_fields(sobject_describe, custom_only: bool = True):
    raw_fields = sobject_describe.get("fields", [])
    fields = []
    for f in raw_fields:
        if custom_only and not f.get("custom", False):
            continue
        field = {
            "name": f["name"],
            "label": f["label"],
            "type": f.get("type"),
            "referenceTo": f.get("referenceTo", []),
        }
        fields.append(field)
    return {
        "name": sobject_describe.get("name"),
        "label": sobject_describe.get("label"),
        "fields": fields,
    }


def build_fields_embedding_map(sobject_fields):
    result = {}
    for f in sobject_fields.get("fields", []):
        text = f["label"]
        if f.get("type") == "reference" and f.get("referenceTo"):
            ref = f["referenceTo"][0]
            text = f"{text} lookup({ref})"
        result[f["name"]] = text
    return result


def build_queryable_sobjects_map(sobjects):
    result = {}
    for s in sobjects:
        if not s.get("queryable", True):
            continue
        result[s["name"]] = f"{s['name']} {s['label']}"
    return result


def execute_soql(soql: str) -> dict:
    """
    Exécute une requête SOQL via l'API Salesforce (credentials du .env).
    """
    from salesforce.client import execute_soql as _execute
    return _execute(soql)

