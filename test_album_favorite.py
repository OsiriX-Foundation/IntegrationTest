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

def test_add_album_to_favorites():
    util.delete_all_ablums(token=env.env_var['USER_1_TOKEN'])
    album = util.new_album(token=env.env_var['USER_1_TOKEN'], data={"name":"new album favorite"})
    env.env_var["ALBUM_ID_1"]=album["album_id"]
    util.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_1"])

def test_get_album_list_filter_by_favorite():
    list_albums = util.list_albums(token=env.env_var.get("USER_1_TOKEN"), params={"favorite":True}, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_1']

def test_remove_album_to_favorites():
    album = util.new_album(token=env.env_var['USER_1_TOKEN'], data={"name":"new album remove favorite"})
    env.env_var["ALBUM_ID_2"]=album["album_id"]
    #add and remove
    util.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    util.remove_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    util.list_albums(token=env.env_var.get("USER_1_TOKEN"), params={"favorite":True}, count=1)
