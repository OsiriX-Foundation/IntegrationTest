import os
import requests
from requests.auth import AuthBase
import json
import urllib
import time
import pytest
import env
import util
import random
import string


def test_init():
    env.initialize()
    print()

def test_get_token():
    print()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

def test_get_albums_empty_list():
    #Test with user 1
    util.delete_all_ablums(token=env.env_var['USER_1_TOKEN'])
    list_albums= util.list_albums(token=env.env_var.get("USER_1_TOKEN"), count=0)
    assert len(list_albums) == 0
    #Test with user 2
    util.delete_all_ablums(token=env.env_var['USER_2_TOKEN'])
    list_albums= util.list_albums(token=env.env_var.get("USER_2_TOKEN"), count=0)
    assert len(list_albums) == 0

def test_new_album():
    data = {"name":"a name"}
    album = util.new_album(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["ALBUM_ID"]=album["album_id"]
    assert album["name"] == "a name"

def test_new_album_empty_name():
    data = {"name":""}
    util.new_album(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)

def test_new_album_limit_size_name():
    #generation of a string containing 271 characters
    str_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=271))
    data ={"name":str_name}
    util.new_album(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)

def test_new_album_limit_size_description():
    #generation of a string containing 2049 characters
    str_desc=''.join(random.choices(string.ascii_uppercase + string.digits, k=2049))
    data ={"name":"name", "description":str_desc}
    util.new_album(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)

def test_new_album_contains_default_params():
    name = "a new album"
    description = "the album description"
    data = {"name":name, "description": description}
    album = util.new_album(token=env.env_var['USER_1_TOKEN'], data=data)
    assert album["name"] == name
    assert album['description'] == description
    assert album["add_user"]== False
    assert album["download_series"]== True
    assert album["send_series"]== True
    assert album["delete_series"]== False
    assert album["add_series"]== True
    assert album["write_comments"]== True

def test_new_album_with_different_param():
    #all parameters False
    name1 = "a new album1"
    description1 = "the album description1"
    data1 = {"name":name1, "description": description1, "addUser":False, "downloadSeries":False, "sendSeries":False, "deleteSeries":False, "addSeries":False,"writeComments":False}
    album1 = util.new_album(token=env.env_var['USER_1_TOKEN'], data=data1)
    assert album1["name"] == name1
    assert album1['description'] == description1
    assert album1["add_user"]== False
    assert album1["download_series"]== False
    assert album1["send_series"]== False
    assert album1["delete_series"]== False
    assert album1["add_series"]== False
    assert album1["write_comments"]== False
    
    #all parameters True
    name2 = "a new album2"
    description2 = "the album description2"
    data2 = {"name":name2, "description": description2, "addUser":True, "downloadSeries":True, "sendSeries":True, "deleteSeries":True, "addSeries":True,"writeComments":True}
    album2 = util.new_album(token=env.env_var['USER_1_TOKEN'], data=data2)
    assert album2["name"] == name2
    assert album2['description'] == description2
    assert album2["add_user"]== True
    assert album2["download_series"]== True
    assert album2["send_series"]== True
    assert album2["delete_series"]== True
    assert album2["add_series"]== True
    assert album2["write_comments"]== True

def test_get_albums_not_found():
    util.get_album(env.env_var.get("USER_1_TOKEN"), "1", 404)

def test_edit_album():
    edit_name= "edit name"
    edit_desc= "edit desc"
    data = {"name":edit_name,"description":edit_desc,"sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    util.edit_album(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), data=data)
    edit_album = util.get_album(env.env_var.get("USER_1_TOKEN"), env.env_var.get("ALBUM_ID"))
    assert edit_album["name"] == edit_name
    assert edit_album['description'] == edit_desc
    assert edit_album["add_user"]== True
    assert edit_album["download_series"]== True
    assert edit_album["send_series"]== True
    assert edit_album["delete_series"]== True
    assert edit_album["add_series"]== True
    assert edit_album["write_comments"]== True
    assert edit_album["notification_new_series"]== False
    assert edit_album["notification_new_comment"]==False

    edit_name= "redit name"
    edit_desc= "redit desc"
    data = {"name":edit_name,"description":edit_desc,"sendSeries":False, "addUser":False, "deleteSeries":True, "notificationNewSeries":True, "notificationNewComment":True}
    util.edit_album(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), data=data)
    edit_album = util.get_album(env.env_var.get("USER_1_TOKEN"), env.env_var.get("ALBUM_ID"))
    assert edit_album["name"] == edit_name
    assert edit_album['description'] == edit_desc
    assert edit_album["add_user"]== False
    assert edit_album["download_series"]== True
    assert edit_album["send_series"]== False
    assert edit_album["delete_series"]== True
    assert edit_album["add_series"]== True
    assert edit_album["write_comments"]== True
    assert edit_album["notification_new_series"]== True
    assert edit_album["notification_new_comment"]==True