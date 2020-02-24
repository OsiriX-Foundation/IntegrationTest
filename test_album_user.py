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


def test_get_user_albums():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    data = {"name":"ablum test user", "description":"desc test album user"}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    album_id_shared=new_album["album_id"]

    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], album_id_shared, count=1)
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], album_id_shared, count=2)
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_3_MAIL"))
    rq_album.get_list_of_user(env.env_var['USER_1_TOKEN'], album_id_shared, count=3)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], album_id_shared, 3)
    
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    #verif admin ou non
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == False

    #test if admin or not