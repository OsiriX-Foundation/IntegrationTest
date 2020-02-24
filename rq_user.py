import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys

################################################################
# USERS
################################################################
def get(token, status_code=200, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/users"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        albums = json.loads(response.content)
        return albums