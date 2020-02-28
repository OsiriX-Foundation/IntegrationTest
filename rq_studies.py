import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys

################################################################
# STUDIES
################################################################
def get_list(token, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    if count != 0:
        assert response.status_code == 200
        assert response.headers.get("X-Total-Count") == str(count)
        studiesList = json.loads(response.content)
        return studiesList
    else:
        assert response.status_code == 204
        assert response.headers.get("X-Total-Count") == str(count)

def stow(token, status_code = 200, file_name = "series/test1.dcm", params = {}):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code