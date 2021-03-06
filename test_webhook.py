import os
import requests
from requests.auth import AuthBase
import json
import urllib
import time
import pytest
import env
import util
import pprint
import rq_album
import rq_studies
import rq_webhook

def test_init():
    env.initialize()

def test_get_token():
    #env.initialize()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

def test_register():
    util.register(token=env.env_var['USER_1_TOKEN'])
    util.register(token=env.env_var['USER_2_TOKEN'])
    util.register(token=env.env_var['USER_3_TOKEN'])

def test_new_album_with_2_users():
    album = rq_album.create(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"] = album["album_id"]
    util.share_series_in_album(token=env.env_var.get("USER_1_TOKEN"), studies_UID="1.2.3.4.5.6", series_UID="1.2.3.4", album_id=env.env_var.get("ALBUM_ID"))

def test_new_webhook1():
    data = {"url":"https://webhook.site/cb3269f7-7184-4f3b-954b-fdd3c356caab", "name":"name", "secret":"1234", "event":["new_series"]}
    webhook = rq_webhook.create(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), data=data)
    env.env_var["WEBHOOK_ID"] = webhook["id"]

#def test_new_webhook2():
#    data = {"url":"http://webhook.site/333a51af-7022-442d-9ee9-c6fe0c6fe14b", "name":"name", "secret":"1234", "new_series":"true", "new_user":"false", }
#    webhook = util.new_webhook(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), data=data)
#    env.env_var["WEBHOOK_ID2"] = webhook["id"]

#def test_new_webhook3():
#    data = {"url":"http://webhook.site/333a51af-7022-442d-9ee9-c6fe0c6fe14b", "name":"name", "secret":"1234", "new_series":"true", "new_user":"false", }
#    webhook = util.new_webhook(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), data=data)
#    env.env_var["WEBHOOK_ID3"] = webhook["id"]

def test_edit_webhook():
    data = {"name":"new name", "secret":"12346578", "event":["new_series", "new_user"]}
    webhook = rq_webhook.edit(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"), data=data)

def test_get_webhook():
    webhook = rq_webhook.get(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"))

def test_get_webhooks():
    webhooks = rq_webhook.get_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"))

def test_add_user():
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), user_id=env.env_var.get("USER_2_MAIL"))
    time.sleep(2)

def test_trigger_user_webhook():
    webhooks = rq_webhook.trigger_user(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"), user_id=env.env_var.get("USER_2_MAIL"))
    time.sleep(2)

#def test_trigger_series_webhook():
#    webhooks = rq_webhook.trigger_series(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"), series_UID="1.2.3.4", study_UID="1.2.3.4.5.6")
#    time.sleep(2)

def test_get_webhook2():
    webhook = rq_webhook.get(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"))

#def test_delete_webhook():
#    rq_webhook.remove(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), webhook_id=env.env_var.get("WEBHOOK_ID"))

#def test_stow():
#    params = {"album": env.env_var.get("ALBUM_ID")}
#    util.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)


def test_delete_all_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])

def test_clean_all_inbox():
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_2_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_3_TOKEN'])
