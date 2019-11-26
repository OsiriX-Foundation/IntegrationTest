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

def test_new_album_src():
    print()
    name = "album src"
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
    env.env_var["ALBUM_ID_SRC"]=album["album_id"]

def test_stow_album_src():
    params = {"album": env.env_var.get("ALBUM_ID_SRC")}
    util.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)

def test_album_studies_list_user1():
    params = {"album": env.env_var.get("ALBUM_ID_SRC")}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)

def test_add_user2():
    util.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID_SRC"), user_id=env.env_var.get("USER_2_MAIL"))

def test_album_studies_list_user2():
    params = {"album": env.env_var.get("ALBUM_ID_SRC")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=1)

def test_new_album_dest():
    print()
    name = "album dst"
    description = "the album description"
    data = {"sendSeries":"false", "name":name, "description": description}
    album = util.new_album(token=env.env_var.get("USER_2_TOKEN"), data=data)
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
    env.env_var["ALBUM_ID_DST"]=album["album_id"]

def test_user2_2_albums():
    res=util.list_albums(token=env.env_var.get("USER_2_TOKEN"), count=2)

def test_album_studies_list_user2_empty():
    params = {"album": env.env_var.get("ALBUM_ID_DST")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

#def test_send_album_to_album_forbidden():
#    util.share_study_in_album_from_album(token=env.env_var.get("USER_1_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), album_src_id=env.env_var.get("ALBUM_ID_SRC"), album_dst_id=env.env_var.get("ALBUM_ID_DST"), status_code=403)
#    params = {"album": env.env_var.get("ALBUM_ID_DST")}
#    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_add_send_series_permission():
    data = {"sendSeries":"true"}
    util.edit_album(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID_SRC"), data=data)

#def test_send_album_to_album():
#    util.share_study_in_album_from_album(token=env.env_var.get("USER_1_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), album_src_id=env.env_var.get("ALBUM_ID_SRC"), album_dst_id=env.env_var.get("ALBUM_ID_DST"))
#    params = {"album": env.env_var.get("ALBUM_ID_DST")}
#    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

#########
### clean
#########

def test_clean():
    util.delete_album(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID_SRC"))
    util.delete_album(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_ID_DST"))
