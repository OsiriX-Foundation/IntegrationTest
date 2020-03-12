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
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":"new album favorite"})
    env.env_var["ALBUM_ID_1"]=album["album_id"]
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_1"])
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_1']
    assert list_albums[0]['is_favorite'] == True

def test_get_album_list_filter_by_favorite():
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"favorite":True}, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_1']
    assert list_albums[0]['is_favorite'] == True

def test_get_album_not_favorite_for_user2():
    #add user2
    album_id_shared = env.env_var['ALBUM_ID_1']
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    list_albums = rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"), params={}, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_1']
    assert list_albums[0]['is_favorite'] == False


def test_remove_album_to_favorites():
    album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":"new album remove favorite"})
    env.env_var["ALBUM_ID_2"]=album["album_id"]
    #add and remove
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    rq_album.remove_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_2"])
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=2)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_2']
    assert list_albums[0]['is_favorite'] == False
    assert list_albums[1]["album_id"] == env.env_var['ALBUM_ID_1']
    assert list_albums[1]['is_favorite'] == True

def test_add_bad_album_in_favorites():
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), "1", status_code=404)

def test_user2_leaves_album():
    rq_album.remove_user(env.env_var.get("USER_2_TOKEN"), env.env_var['ALBUM_ID_1'],env.env_var.get("USER_2_MAIL"))

    #check user 1 albums
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=2)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_2']
    assert list_albums[0]['is_favorite'] == False
    assert list_albums[1]["album_id"] == env.env_var['ALBUM_ID_1']
    assert list_albums[1]['is_favorite'] == True
    #check user 2 albums
    rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"), params={}, count=0)

def test_a_not_member_user_try_to_add_to_favorites():
    rq_album.add_favorite(env.env_var.get("USER_2_TOKEN"), env.env_var['ALBUM_ID_1'], status_code=404)


def test_remove_favorite_with_bad_album_id():
    rq_album.remove_favorite(env.env_var.get("USER_2_TOKEN"), "1", status_code=404)

def test_remove_favorite_with_not_user_member():
    rq_album.remove_favorite(env.env_var.get("USER_2_TOKEN"), env.env_var["ALBUM_ID_1"], status_code=404)
    #remove all created albums
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
