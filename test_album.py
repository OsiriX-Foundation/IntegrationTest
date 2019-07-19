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


def test_new_album():
    env.initialize()
    print()
    name = "the album name"
    description = "the album description"
    data = {"sendSeries":"false", "name":name, "description": description}
    album=util.new_album(token=env.USER_1_TOKEN, data=data)
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
    util.stow(token=env.USER_1_TOKEN)

def test_get_studies_list_from_inbox():
    env.initialize()
    params = {"inbox": "True"}
    util.studies_list(token=env.USER_1_TOKEN,params=params, count=1)
