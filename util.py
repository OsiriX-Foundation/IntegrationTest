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

def urlencode(data):
    return urllib.parse.urlencode(data)


def stow(token, status_code = 200, file_name = "testStudy.dcm", params = {}):
    env.initialize()
    print()
    request_url = env.URL + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    print_request("POST", response, request_url)
    assert response.status_code == status_code

def new_album(token, data={"name":"a name"}):
    env.initialize()
    print()
    request_url = env.URL + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == 201
    album = json.loads(response.content)
    return album

def studies_list(token, params={}, count=1):
    env.initialize()
    print()
    request_url = env.URL + "/studies"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    assert response.status_code == 200
    assert response.headers.get("X-Total-Count") == str(count)
    studiesList = json.loads(response.content)
    return studiesList
