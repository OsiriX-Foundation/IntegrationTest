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
    token = util.get_token(username="karnak", password="karnak")
    env.env_var["USER_KARNAK_TOKEN"] = token

def test_register():
    util.register(token=env.env_var['USER_1_TOKEN'])
    util.register(token=env.env_var['USER_2_TOKEN'])
    util.register(token=env.env_var['USER_3_TOKEN'])

def test_clean_kheops():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_KARNAK_TOKEN'], user_id=env.env_var['USER_KARNAK_MAIL'])

    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
