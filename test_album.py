import os
import requests
from requests.auth import AuthBase
import json
import urllib
import time
import pytest
import env
import util


def test_init():
    env.initialize()
    print()

def test_get_token():
    #env.initialize()
    print()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

def test_new_album():
    print()
    name = "the album name"
    description = "the album description"
    data = {"sendSeries":"false", "name":name, "description": description}
    album = util.new_album(token=env.env_var.get("USER_1_TOKEN"), data=data)
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
    util.stow(token=env.env_var.get("USER_1_TOKEN"))

def test_get_studies_list_from_inbox():
    params = {"inbox": "True"}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"),params=params, count=1)
