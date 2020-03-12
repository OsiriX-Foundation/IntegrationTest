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

def test_create_new_album():
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])

    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'])
    env.env_var["ALBUM_ID_SOURCE"]=new_album["album_id"]

def test_stow():
    params = {"album": env.env_var["ALBUM_ID_SOURCE"]}
    #insert 5 differents series in album
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test1.dcm", params=params)
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test2.dcm", params=params)
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test3.dcm", params=params)
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test4.dcm", params=params)
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test4_1.dcm", params=params)
    rq_studies.stow(token=env.env_var["USER_1_TOKEN"], file_name = "series/test5.dcm", params=params)


def test_studies_list():
    params = {"album": env.env_var["ALBUM_ID_SOURCE"]}
    rq_studies.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=5)


def test_create_new_album_where_share_studies():
    new_album = rq_album.create(token=env.env_var['USER_2_TOKEN'], data={"name":"share study"})

    env.env_var["ALBUM_ID_DEST"]=new_album["album_id"]
    params = {"album": env.env_var["ALBUM_ID_DEST"]}
    #study is empty
    rq_studies.get_list(token=env.env_var["USER_2_TOKEN"], params=params, count=0)


def test_share_study_in_album():
    rq_album.add_user(env.env_var["USER_2_TOKEN"], env.env_var["ALBUM_ID_DEST"], env.env_var["USER_1_MAIL"])
    params = {"album": env.env_var["ALBUM_ID_SOURCE"]}
    rq_studies.add_in_album(env.env_var["USER_1_TOKEN"], params, env.env_var["STUDY_UID4_1"], env.env_var["ALBUM_ID_DEST"])
    rq_studies.get_list(token=env.env_var["USER_2_TOKEN"], params={"album": env.env_var["ALBUM_ID_DEST"]}, count=1)

def test_delete_albums():
    #delete use 1 albums
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
#def test_share_study_in inbox():
