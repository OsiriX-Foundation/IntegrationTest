import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys


def create(token, data, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/capabilities"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        capability_token = json.loads(response.content)
        return capability_token

def introspect(token, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/token/introspect"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"token": token}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        introspect = json.loads(response.content)
        return introspect
