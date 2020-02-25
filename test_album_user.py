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
    albums_list = rq_album.get(token=env.env_var["USER_1_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"],  status_code=200, params={"includeUsers":True})
    assert len(albums_list["users"])==albums_list["number_of_users"]
    assert albums_list["users"][0]["email"] == env.env_var["USER_3_MAIL"]
    assert albums_list["users"][1]["email"] == env.env_var["USER_1_MAIL"]
    assert albums_list["users"][2]["email"] == env.env_var["USER_2_MAIL"]

def test_upgrade_user_to_admin():
    rq_album.upgrade_user_to_admin(token=env.env_var["USER_1_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == True

def test_downgrade_admin_to_user():
    rq_album.downgrade_admin_to_user(token=env.env_var["USER_1_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == False

def test_remove_user_in_album():
    #remove user
    rq_album.remove_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=2, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True

def test_user_self_add_but_not_member():
    rq_album.add_user(env.env_var["USER_2_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_2_MAIL"], status_code=404)
    
def test_add_user_in_album():    
    rq_album.add_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_2_MAIL"], status_code=201)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == False


def test_that_the_user_not_admin_cannot_become_admin():
    rq_album.upgrade_user_to_admin(token=env.env_var["USER_2_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=403)
    rq_album.upgrade_user_to_admin(token=env.env_var["USER_3_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=403)

def test_that_the_user_not_admin_cannot_downgrade_admin():
    rq_album.downgrade_admin_to_user(token=env.env_var["USER_2_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_1_MAIL"], status_code=403)
    rq_album.downgrade_admin_to_user(token=env.env_var["USER_3_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_1_MAIL"], status_code=403)

def test_add_user_directly_admin_in_album(): 
    #remove user
    rq_album.remove_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=2, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True

    rq_album.upgrade_user_to_admin(token=env.env_var["USER_1_TOKEN"], album_id=env.env_var["ALBUM_ID_SHARED"], user_id=env.env_var["USER_2_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=3, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_1_MAIL"]
    assert user_in_album[2]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True
    assert user_in_album[2]["is_admin"] == True

def test_edit_album_with_new_admin_add_in_album():
    edit_name= "edit name"
    edit_desc= "edit desc"
    data = {"name":edit_name,"description":edit_desc,"sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var['ALBUM_ID_SHARED'], data=data, status_code=200)
    edit_album = rq_album.get(env.env_var.get("USER_2_TOKEN"), env.env_var['ALBUM_ID_SHARED'])
    assert edit_album["name"] == edit_name
    assert edit_album['description'] == edit_desc
    assert edit_album["add_user"]== True
    assert edit_album["download_series"]== True
    assert edit_album["send_series"]== True
    assert edit_album["delete_series"]== True
    assert edit_album["add_series"]== True
    assert edit_album["write_comments"]== True
    assert edit_album["notification_new_series"]== False
    assert edit_album["notification_new_comment"]==False

def test_edit_album_forbidden_when_not_admin():
    data = {"name":"edit name","description":"edit desc","sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_3_TOKEN"), album_id=env.env_var['ALBUM_ID_SHARED'], data=data, status_code=403)

def test_remove_first_user_admin_in_album():
    #remove user
    rq_album.remove_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_1_MAIL"], status_code=204)
    user_in_album = rq_album.get_list_of_user(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_SHARED'], count=2, status_code=200)
    assert user_in_album[0]["email"] == env.env_var["USER_3_MAIL"]
    assert user_in_album[1]["email"] == env.env_var["USER_2_MAIL"]
    assert user_in_album[0]["is_admin"] == False
    assert user_in_album[1]["is_admin"] == True

def test_add_bad_user():
    rq_album.add_user(env.env_var["USER_2_TOKEN"], env.env_var["ALBUM_ID_SHARED"], "111111", status_code=404)

def test_that_all_user_quit_album():
    rq_album.remove_user(env.env_var["USER_2_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_2_MAIL"], status_code=204)
    rq_album.remove_user(env.env_var["USER_3_TOKEN"], env.env_var["ALBUM_ID_SHARED"], env.env_var["USER_3_MAIL"], status_code=204)

