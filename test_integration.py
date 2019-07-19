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
import util

STUDY_UID = "2.16.840.1.113669.632.20.1211.10000314223"
SERIES_UID = "1.3.12.2.1107.5.1.4.48545.30000006100307470634300004693"

def test_new_album():
    env.initialize()
    print()
    request_url = env.URL + "/albums"
    headers = {"Authorization": "Bearer "+ env.USER_1_TOKEN, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    name = "the album name"
    description = "the album description"
    data = {"sendSeries":"false", "name":name, "description": description}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    album=json.loads(response.content)
    assert response.status_code == 201
    assert album["name"] == name
    assert album["description"] == description
    assert album["send_series"] == False
    assert album["download_series"] == True
    assert album["add_user"] == False
    assert album["delete_series"] == False
    assert album["write_comments"] == True
    assert album["is_favorite"] == False
    assert album["add_series"] == True
    assert album["notification_new_series"] == True
    assert album["notification_new_comment"] == True
    assert album["is_admin"] == True
    assert album["number_of_users"] == 1
    assert album["number_of_comments"] == 0
    assert album["number_of_studies"] == 0
    assert album["modalities"] == []

def test_stow():
    env.initialize()
    print()
    # STOW
    util.stow(token = env.USER_1_TOKEN)


def test_get_studies_list_from_inbox():
    env.initialize()
    print()
    # get studies list from inbox
    request_url = env.URL + "/studies"
    headers = {"Authorization": "Bearer "+ env.USER_1_TOKEN}
    params = {"inbox": "True"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    #assert response.status_code == 200
    assert response.headers.get("X-Total-Count") == "1"
