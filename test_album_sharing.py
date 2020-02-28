import rq_album
import rq_user
import rq_studies
import env
import util
import random
import string
import json

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

def test_new_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'])

    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'])
    env.env_var["ALBUM_ID_SHARING"]=new_album["album_id"]

def test_stow():
    params = {"album": env.env_var.get("ALBUM_ID_SHARING")}
    #insert 5 differents series in album
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), file_name = "series/test1.dcm", params=params)
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), file_name = "series/test2.dcm", params=params)
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), file_name = "series/test3.dcm", params=params)
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), file_name = "series/test4.dcm", params=params)
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), file_name = "series/test5.dcm", params=params)

def test_album_studies_list():
    params = {"album": env.env_var.get("ALBUM_ID_SHARING")}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=5)

#def test_get_events_mutation_when_create_album():
    