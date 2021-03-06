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
import rq_capability_token

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

def test_new_album():
    album = rq_album.create(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"] = album["album_id"]

def test_stow():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)

def test_album_studies_list():
    params = {"album": env.env_var.get("ALBUM_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)

def test_inbox_user1_studies_list_0():
    params = {"inbox": True}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=0)

def test_create_capability_token():
    data={"title": "name", "scope_type": "album", "album": env.env_var.get("ALBUM_ID"), "read_permission": True, "appropriate_permission": False, "download_permission": True, "write_permission": True}
    capability_token = rq_capability_token.create(token=env.env_var.get("USER_1_TOKEN"), data=data)
    env.env_var["CAPABILITY_TOKEN"] = capability_token["secret"]

#########
### share with another album (series)
#########

def test_new_album_destination():
    album = rq_album.create(token=env.env_var.get("USER_2_TOKEN"))
    env.env_var["ALBUM_DESTINATION_ID"] = album["album_id"]

def test_album_destination_studies_list():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list():
    params = {"inbox": True}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_send_with_token_to_an_album():
    util.share_series_in_album(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"), X_Authorization_Source=env.env_var.get("CAPABILITY_TOKEN"), status_code=404)

def test_album_destination_studies_list_0():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list_0():
    params = {"inbox": True}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_delete_album():
    rq_album.delete(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"))

def test_user2_studies_list():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

#########
### share with another album (study)
#########

def test_new_album_destination_study():
    album = rq_album.create(token=env.env_var.get("USER_2_TOKEN"))
    env.env_var["ALBUM_DESTINATION_ID"] = album["album_id"]

def test_album_destination_studies_list_study():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list_study():
    params = {"inbox": True}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_send_with_token_to_an_album_study():
    util.share_study_in_album(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"), X_Authorization_Source=env.env_var.get("CAPABILITY_TOKEN"), status_code=403)

def test_album_destination_studies_list_1_study():
    params = {"album": env.env_var.get("ALBUM_DESTINATION_ID")}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_inbox_user2_studies_list_0_study():
    params = {"inbox": True}
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), params=params, count=0)

def test_delete_album_study():
    rq_album.delete(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_DESTINATION_ID"))

def test_user2_studies_list_study():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

#########
### share with another user (series)
#########

def test_user3_studies_list_0_series():
    rq_studies.get_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

def test_send_with_token_to_user_3_series():
    util.share_series_with_user(token=env.env_var.get("CAPABILITY_TOKEN"), user="tata@gmail.com", studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), status_code=404)

def test_user3_studies_list_1_series():
    rq_studies.get_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

#########
### share with another user (study)
#########

def test_user3_studies_list_0_study():
    rq_studies.get_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

def test_send_with_token_to_user_3_study():
    util.share_study_with_user(token=env.env_var.get("CAPABILITY_TOKEN"), user="tata@gmail.com", studies_UID=env.env_var.get("STUDY_UID"), status_code=403)

def test_user3_studies_list_1_study():
    rq_studies.get_list(token=env.env_var.get("USER_3_TOKEN"), count=0)

#########
### appropriate with token (study)
#########

def test_user2_studies_list_0_appropriate_study():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

def test_user2_appropriate_study():
    util.appropriate_study(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), X_Authorization_Source=env.env_var.get("CAPABILITY_TOKEN"), status_code=403)

def test_user2_studies_list_1_appropriate_study():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

#########
### appropriate with token (series)
#########

def test_user2_studies_list_0_appropriate_series():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

def test_user2_appropriate_series():
    util.appropriate_series(token=env.env_var.get("USER_2_TOKEN"), studies_UID=env.env_var.get("STUDY_UID"), series_UID=env.env_var.get("SERIES_UID"), X_Authorization_Source=env.env_var.get("CAPABILITY_TOKEN"), status_code=404)

def test_user2_studies_list_1_appropriate_series():
    rq_studies.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)

def test_delete_all_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])

def test_clean_all_inbox():
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_2_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_3_TOKEN'])
