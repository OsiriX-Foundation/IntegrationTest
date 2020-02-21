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
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":"new album favorite"})
    env.env_var["ALBUM_ID_1"]=album["album_id"]
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_1"])

def test_get_album_list_filter_by_favorite():
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"favorite":True}, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_1']

def test_remove_album_to_favorites():
    album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":"new album remove favorite"})
    env.env_var["ALBUM_ID_2"]=album["album_id"]
    #add and remove
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    rq_album.remove_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"favorite":True}, count=1)
