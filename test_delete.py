import os
import requests
from requests.auth import AuthBase
import json
import urllib
import time
import pytest
import env
import util
import rq_album
import rq_studies

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
    album = rq_album.create(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"] = album["album_id"]

def test_get_studies_list_from_user3():
    params = {"inbox": "true"}
    rq_studies.get_list(token=env.env_var.get("USER_3_TOKEN"),params=params, count=0)

def test_stow():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)

def test_create_capability_token_read_only():
    data={"title": "title", "scope_type": "album", "album": env.env_var.get("ALBUM_ID"), "read_permission": True, "appropriate_permission": True, "download_permission": False, "write_permission": False}
    capability_token = util.new_token(token=env.env_var.get("USER_1_TOKEN"), data=data)
    env.env_var["CAPABILITY_TOKEN_READ_ONLY"] = capability_token["secret"]

def test_send_with_token_to_user_3_study():
    util.share_study_with_user(token=env.env_var.get("CAPABILITY_TOKEN_READ_ONLY"), user="3685d976-f1d6-443c-95d4-95ee4b749878", studies_UID=env.env_var.get("STUDY_UID"))

def test_get_studies_list_from_album():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"),params=params, count=1)

def test_create_capability_token_read_write():
    data={"title": "title", "scope_type": "album", "album": env.env_var.get("ALBUM_ID"), "read_permission": True, "appropriate_permission": True, "download_permission": False, "write_permission": True}
    capability_token = util.new_token(token=env.env_var.get("USER_1_TOKEN"), data=data)
    env.env_var["CAPABILITY_TOKEN_READ_WRITE"] = capability_token["secret"]

def test_delete_with_token_read_write():
    util.delete_series_from_album(token=env.env_var.get("CAPABILITY_TOKEN_READ_WRITE"), album_id=env.env_var.get("ALBUM_ID"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), status_code=204)

def test_delete_all_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'])