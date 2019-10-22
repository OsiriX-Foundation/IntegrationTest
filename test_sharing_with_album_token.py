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

def test_get_token():
    #env.initialize()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

def test_new_album():
    album = util.new_album(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"] = album["album_id"]

def test_stow():
    params = {"album": env.env_var.get("ALBUM_ID")}
    util.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)

def test_album_studies_list():
    params = {"album": env.env_var.get("ALBUM_ID")}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)

def test_inbox_user1_studies_list_0():
    params = {"inbox": True}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=0)

def test_create_capability_token():
    data={"title": "name", "scope_type": "album", "album": env.env_var.get("ALBUM_ID"), "read_permission": True, "appropriate_permission": True, "download_permission": False, "write_permission": False}
    capability_token = util.new_token(token=env.env_var.get("USER_1_TOKEN"), data=data)
    env.env_var["CAPABILITY_TOKEN"] = capability_token["secret"]

#########
### share with another album (series)
#########

def test_new_album_destination():
    album = util.new_album(token=env.env_var.get("USER_2_TOKEN"))
    env.env_var["ALBUM_DESTINATION_ID"] = album["album_id"]

def test_album_destination_studies_list():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list():
    params = {"inbox": True}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_send_with_token_to_an_album():
    util.share_series_in_album(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"), X_Token_Source=env.env_var.get("CAPABILITY_TOKEN"))

def test_album_destination_studies_list_1():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=1)

def test_inbox_user2_studies_list_0():
    params = {"inbox": True}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_delete_album():
    util.delete_album(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"))

def test_user2_studies_list():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

#########
### share with another album (study)
#########

def test_new_album_destination_study():
    album = util.new_album(token=env.env_var.get("USER_2_TOKEN"))
    env.env_var["ALBUM_DESTINATION_ID"] = album["album_id"]

def test_album_destination_studies_list_study():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list_study():
    params = {"inbox": True}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_send_with_token_to_an_album_study():
    util.share_study_in_album(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"), X_Token_Source=env.env_var.get("CAPABILITY_TOKEN"))

def test_album_destination_studies_list_1_study():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=1)

def test_inbox_user2_studies_list_0_study():
    params = {"inbox": True}
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_delete_album_study():
    util.delete_album(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"))

def test_user2_studies_list_study():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

#########
### share with another user (series)
#########

def test_user3_studies_list_0_series():
    util.studies_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

def test_send_with_token_to_user_3_series():
    util.share_series_with_user(token=env.env_var.get("CAPABILITY_TOKEN"), user="tata@gmail.com", studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"))

def test_user3_studies_list_1_series():
    util.studies_list(token=env.env_var.get("USER_3_TOKEN"), count=1)

def test_remove_series_from_inbox_user_3_series():
    util.delete_series_from_inbox(token=env.env_var.get("USER_3_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"))

#########
### share with another user (study)
#########

def test_user3_studies_list_0_study():
    util.studies_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

def test_send_with_token_to_user_3_study():
    util.share_study_with_user(token=env.env_var.get("CAPABILITY_TOKEN"), user="tata@gmail.com", studies_UID=env.env_var.get("STUDY_UID"))

def test_user3_studies_list_1_study():
    util.studies_list(token=env.env_var.get("USER_3_TOKEN"), count=1)

def test_remove_series_from_inbox_user_3_study():
    util.delete_series_from_inbox(token=env.env_var.get("USER_3_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"))

#########
### appropriate with token (study)
#########

def test_user2_studies_list_0_appropriate_study():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

def test_user2_appropriate_study():
    util.appropriate_study(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), X_Token_Source=env.env_var.get("CAPABILITY_TOKEN"))

def test_user2_studies_list_1_appropriate_study():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=1)

def test_remove_series_from_inbox_user_2_appropriate_study():
    util.delete_series_from_inbox(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"))

#########
### appropriate with token (series)
#########

def test_user2_studies_list_0_appropriate_series():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

def test_user2_appropriate_series():
    util.appropriate_series(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), X_Token_Source=env.env_var.get("CAPABILITY_TOKEN"))

def test_user2_studies_list_1_appropriate_series():
    util.studies_list(token=env.env_var.get("USER_2_TOKEN"), count=1)

def test_remove_series_from_inbox_user_2_appropriate_series():
    util.delete_series_from_inbox(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"))
