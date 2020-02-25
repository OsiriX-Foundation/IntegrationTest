import rq_album
import rq_user
import env
import util
import random
import string


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


def test_get_list_of_user_in_albums():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    data = {"name":"ablum test user", "description":"desc test album user"}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var['ALBUM_ID_SHARED']=new_album["album_id"]

    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], env.env_var['ALBUM_ID_SHARED'], count=1)
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id= env.env_var['ALBUM_ID_SHARED'], user_id=env.env_var.get("USER_2_MAIL"))
    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], env.env_var['ALBUM_ID_SHARED'], count=2)
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_SHARED'], user_id=env.env_var.get("USER_3_MAIL"))
    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], env.env_var['ALBUM_ID_SHARED'], count=3)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], 3)
    
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    #verif admin ou non
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == False

def test_get_users_in_album_when_not_admin():
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    #verif admin ou non
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == False


def test_get_album_with_user_list():
    albums_list = rq_album.get(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var["ALBUM_ID_SHARED"],  status_code=200, params={"includeUsers":True})
    assert len(albums_list["users"])==albums_list["number_of_users"]
    assert albums_list["users"][0]["email"] == env.env_var["USER_3_MAIL"]
    assert albums_list["users"][1]["email"] == env.env_var["USER_1_MAIL"]
    assert albums_list["users"][2]["email"] == env.env_var["USER_2_MAIL"]

def test_upgrade_user_to_admin():
    rq_album.upgrade_user_to_admin(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == True
        
def test_reset():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'])
