import os
import requests
import numpy
from requests.auth import AuthBase
import json
import urllib
from threading import Thread
import time
import pytest
import env


def print_request(methode, response, url):
    print("\t" + methode + " " + url + " ["+ str(response.status_code) + " " + requests.status_codes._codes[response.status_code][0].upper() + ", " + str(int(response.elapsed.total_seconds()*1000))+"ms]")
    print_info(response.content)

def urlencode(data):
    return urllib.parse.urlencode(data)

def print_info(info):
    if env.env_var.get("PRINT_INFO"):
        print(info)


def stow(token, status_code = 200, file_name = "testStudy.dcm", params = {}):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    print_request("POST", response, request_url)
    assert response.status_code == status_code

def new_album(token, data={"name":"a name"}, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        album = json.loads(response.content)
        return album

def studies_list(token, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    assert response.status_code == 200
    assert response.headers.get("X-Total-Count") == str(count)
    studiesList = json.loads(response.content)
    return studiesList

def get_token(username, password, realm="travis", client_id="loginConnect"):
    well_known_url = "https://keycloak.kheops.online/auth/realms/"+str(realm)+"/.well-known/openid-configuration"
    response = requests.get(well_known_url)
    assert response.status_code == 200
    well_known = json.loads(response.content)
    assert "token_endpoint" in well_known

    token_endpoint = well_known["token_endpoint"]

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "password", "username": username, "password": password, "client_id":client_id}
    response = requests.post(token_endpoint, headers=headers, data=data)
    token_response = json.loads(response.content)
    return token_response["access_token"]

################################################################
# REPORT PROVIDER
################################################################

def new_report_provider(token, data, album_id, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums/"+str(album_id)+"/reportproviders"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        reportprovider = json.loads(response.content)
        return reportprovider

def report_provider_list(token, album_id, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/albums/"+str(album_id)+"/reportproviders"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    assert response.status_code == 200
    assert response.headers.get("X-Total-Count") == str(count)
    report_providers = json.loads(response.content)
    return report_providers
