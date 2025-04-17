import requests
from typing import List, Dict, Optional

CRUD_SERVICE_URL = "http://crudservice:8000"

def get_all_managers() -> List[Dict]:
    response = requests.get(f"{CRUD_SERVICE_URL}/")
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to fetch readers from CRUD service")

def make_report():
    managers = get_all_managers()
    res = {str(manager["name"]): manager["contracts_count"] for manager in managers}
    return res

def get_report_data() -> Dict:
    return make_report()