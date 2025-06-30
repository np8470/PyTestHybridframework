import requests

BASE_URL = "https://dummyjson.com"

@staticmethod
def get_user(user_id, return_status=False):
    response = requests.get(f"{BASE_URL}/users/{user_id}", verify=False)
    if return_status:
        return response.json(), response.status_code
    return response.json()
    response.raise_for_status()
    #return response.json()

def create_user(payload, return_status=False):
    #response = requests.request("POST", BASE_URL, json=payload)
    response = requests.post(f"{BASE_URL}/users/add", json=payload, verify=False)
    response.raise_for_status()
    #return response.json()
    if return_status:
        return response.json(), response.status_code
    return response.json()

def update_user(user_id, payload, return_status=False):
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload, verify=False)
    response.raise_for_status()
    #return response.json()
    if return_status:
        return response.json(), response.status_code
    return response.json()

def delete_user(user_id, return_status=False):
    response = requests.delete(f"{BASE_URL}/users/{user_id}", verify=False)
    response.raise_for_status()
    if return_status:
        return response.json(), response.status_code
    return response.json()