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
    request_url = env.URL + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    print_request("POST", response, request_url)
    assert response.status_code == status_code
