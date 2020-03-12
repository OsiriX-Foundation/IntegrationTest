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


#  Initialisation :
#  Creation d'un album Karnk avec un admin (Karnak) et 3 utilisateurs (user 1, 2 et 3) + un token read write pour karnak
#  Création d'un album A avec un admin (user 1) qui est aussi membre de l'album karnak + un token write only pour karnak
#  Création d'un album B avec un admin (user 2) qui est aussi membre de l'album karnak + un token write only pour karnak
#  Création d'un album C avec un admin (user 3) qui est aussi membre de l'album karnak + un token write only pour karnak

def test_create_karnak_album():
    data = {"name":"karnak album", "addUser":False, "downloadSeries":False, "sendSeries":True, "deleteSeries":False, "addSeries":False,"writeComments":False}
    new_album = rq_album.create(token=env.env_var['USER_KARNAK_TOKEN'], data=data)
    env.env_var["ALBUM_ID_KARNAK"]=new_album["album_id"]
    rq_album.add_user(token=env.env_var['USER_KARNAK_TOKEN'], album_id=env.env_var['ALBUM_ID_KARNAK'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.add_user(token=env.env_var['USER_KARNAK_TOKEN'], album_id=env.env_var['ALBUM_ID_KARNAK'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.add_user(token=env.env_var['USER_KARNAK_TOKEN'], album_id=env.env_var['ALBUM_ID_KARNAK'], user_id=env.env_var['USER_3_MAIL'])

def test_create_karnak_token_r_w():
    data = {"title":"karnak token read write", "scope_type":"album", "album":env.env_var['ALBUM_ID_KARNAK'], "read_permission":True, "appropriate_permission":True, "download_permission":False, "write_permission":True}
    new_token = util.new_token(token=env.env_var['USER_KARNAK_TOKEN'], data=data)
    env.env_var["TOKEN_RW_KARNAK"]=new_token["secret"]

def test_create_album_A():
    data = {"name":"album A"}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["ALBUM_ID_A"]=new_album["album_id"]

def test_create_album_A_token_w():
    data = {"title":"album A token write only", "scope_type":"album", "album":env.env_var['ALBUM_ID_A'], "read_permission":False, "write_permission":True}
    new_token = util.new_token(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["TOKEN_W_ALBUM_A"]=new_token["secret"]

def test_create_album_B():
    data = {"name":"album B"}
    new_album = rq_album.create(token=env.env_var['USER_2_TOKEN'], data=data)
    env.env_var["ALBUM_ID_B"]=new_album["album_id"]

def test_create_album_B_token_w():
    data = {"title":"album B token write only", "scope_type":"album", "album":env.env_var['ALBUM_ID_B'], "read_permission":False, "write_permission":True}
    new_token = util.new_token(token=env.env_var['USER_2_TOKEN'], data=data)
    env.env_var["TOKEN_W_ALBUM_B"]=new_token["secret"]

def test_create_album_C():
    data = {"name":"album C"}
    new_album = rq_album.create(token=env.env_var['USER_3_TOKEN'], data=data)
    env.env_var["ALBUM_ID_C"]=new_album["album_id"]

def test_create_album_C_token_w():
    data = {"title":"album C token write only", "scope_type":"album", "album":env.env_var['ALBUM_ID_C'], "read_permission":False, "write_permission":True}
    new_token = util.new_token(token=env.env_var['USER_3_TOKEN'], data=data)
    env.env_var["TOKEN_W_ALBUM_C"]=new_token["secret"]


#  Etape 1 :
#  Poster une etude dans l'album karnak avec le token R/W sur l'album karnak
def test_stow_in_karnak():
    params = {"album": env.env_var["ALBUM_ID_KARNAK"]}
    rq_studies.stow(token=env.env_var["TOKEN_RW_KARNAK"], file_name = "series/test1.dcm", params=params)
    rq_studies.get_list(token=env.env_var['USER_KARNAK_TOKEN'], params=params, count=1)

#  Etape 2 :
#  Partager l'etude avec l'album A en utilisant le token karnak R/W et le token W de l'album A
#  Partager l'etude avec l'album B en utilisant le token karnak R/W et le token W de l'album B
def test_send_to_album_A():
    appropriate_series(token=env.env_var["TOKEN_W_ALBUM_A"], studies_UID=env.env_var["STUDY_UID1"], series_UID=env.env_var["SERIES_UID1"], X_Authorization_Source=env.env_var["TOKEN_RW_KARNAK"])
    params = {"album": env.env_var["ALBUM_ID_A"]}
    rq_studies.get_list(token=env.env_var['USER_1_TOKEN'], params=params, count=1)

def test_send_to_album_B():
    appropriate_series(token=env.env_var["TOKEN_W_ALBUM_B"], studies_UID=env.env_var["STUDY_UID1"], series_UID=env.env_var["SERIES_UID1"], X_Authorization_Source=env.env_var["TOKEN_RW_KARNAK"])
    params = {"album": env.env_var["ALBUM_ID_B"]}
    rq_studies.get_list(token=env.env_var['USER_2_TOKEN'], params=params, count=1)

#  Etape 3 :
#  L'utilisateur 3 va lui meme chercher l'etude dans l'album karnak pour la mettre dans son album
def test_appropriate_from_karnak_album():
    share_study_in_album_from_album(token=env.env_var['USER_3_TOKEN'], studies_UID=env.env_var['STUDY_UID1'], album_src_id=env.env_var['ALBUM_ID_KARNAK'], album_dst_id=env.env_var['ALBUM_ID_C'])
    params = {"album": env.env_var["ALBUM_ID_C"]}
    rq_studies.get_list(token=env.env_var['USER_3_TOKEN'], params=params, count=1)





def test_clean_kheops():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_KARNAK_TOKEN'])
