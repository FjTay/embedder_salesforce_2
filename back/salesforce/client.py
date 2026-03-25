from pathlib import Path

from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def connect():
    import os

    return Salesforce(
        username=os.environ["SF_USERNAME"],
        password=os.environ["SF_PASSWORD"],
        security_token=os.environ["SF_SECURITY_TOKEN"],
        domain=os.environ.get("SF_LOGIN_DOMAIN", "login"),
    )


def global_describe():
    sf = connect()
    result = sf.describe()
    return result


def describe_sobject(object_name):
    sf = connect()
    sobject = getattr(sf, object_name)
    return sobject.describe()


def execute_soql(soql: str) -> dict:
    """
    Exécute une requête SOQL via l'API Salesforce (credentials du .env).

    Returns:
        Dict avec 'success', 'result' (liste des records) ou 'error'
    """
    try:
        sf = connect()
        result = sf.query(soql)
        records = result.get("records", [])
        return {"success": True, "result": records}
    except Exception as e:
        return {"success": False, "error": str(e)}

