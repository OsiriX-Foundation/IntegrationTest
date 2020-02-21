import rq_album
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

#################### BASIC ALBUM TEST#############################
def test_get_albums_empty_list():
    #Test with user 1
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'])
    list_albums= rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), count=0)
    assert len(list_albums) == 0
    #Test with user 2
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'])
    list_albums= rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"), count=0)
    assert len(list_albums) == 0

def test_new_album():
    data = {"name":"a name"}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["ALBUM_ID_1"]=new_album["album_id"]
    assert new_album["name"] == "a name"

def test_new_album_empty_name():
    data = {"name":""}
    rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)

def test_new_album_limit_size_name():
    #generation of a string containing 271 characters
    str_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=271))
    data ={"name":str_name}
    rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)

def test_new_album_limit_size_description():
    #generation of a string containing 2049 characters
    str_desc=''.join(random.choices(string.ascii_uppercase + string.digits, k=2049))
    data ={"name":"name", "description":str_desc}
    rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data, status_code=400)
   

def test_new_album_contains_default_params():
    name = "a new album"
    description = "the album description"
    data = {"name":name, "description": description}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["ALBUM_ID_2"]=new_album["album_id"]
    assert new_album["name"] == name
    assert new_album['description'] == description
    assert new_album["add_user"]== False
    assert new_album["download_series"]== True
    assert new_album["send_series"]== True
    assert new_album["delete_series"]== False
    assert new_album["add_series"]== True
    assert new_album["write_comments"]== True

def test_new_album_with_different_param():
    #all parameters False
    name1 = "a new album1"
    description1 = "the album description1"
    data1 = {"name":name1, "description": description1, "addUser":False, "downloadSeries":False, "sendSeries":False, "deleteSeries":False, "addSeries":False,"writeComments":False}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data1)
    env.env_var["ALBUM_ID_3"]=new_album["album_id"]
    assert new_album["name"] == name1
    assert new_album['description'] == description1
    assert new_album["add_user"]== False
    assert new_album["download_series"]== False
    assert new_album["send_series"]== False
    assert new_album["delete_series"]== False
    assert new_album["add_series"]== False
    assert new_album["write_comments"]== False
    
    #all parameters True
    name2 = "a new album2"
    description2 = "the album description2"
    data2 = {"name":name2, "description": description2, "addUser":True, "downloadSeries":True, "sendSeries":True, "deleteSeries":True, "addSeries":True,"writeComments":True}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data2)
    env.env_var["ALBUM_ID_4"]=new_album["album_id"]
    assert new_album["name"] == name2
    assert new_album['description'] == description2
    assert new_album["add_user"]== True
    assert new_album["download_series"]== True
    assert new_album["send_series"]== True
    assert new_album["delete_series"]== True
    assert new_album["add_series"]== True
    assert new_album["write_comments"]== True

def test_get_albums_not_found():
    rq_album.get(env.env_var.get("USER_1_TOKEN"), "1", 404)

################EDIT ALBUM TEST##########################
def test_edit_album():
    edit_name= "edit name"
    edit_desc= "edit desc"
    data = {"name":edit_name,"description":edit_desc,"sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID_1"), data=data)
    edit_album = rq_album.get(env.env_var.get("USER_1_TOKEN"), env.env_var.get("ALBUM_ID_1"))
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

    #re edit
    edit_name= "re edit name"
    edit_desc= "re edit desc"
    data = {"name":edit_name,"description":edit_desc,"sendSeries":False, "addUser":False, "deleteSeries":True, "notificationNewSeries":True, "notificationNewComment":True}
    rq_album.edit(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID_1"), data=data)
    edit_album = rq_album.get(env.env_var.get("USER_1_TOKEN"), env.env_var.get("ALBUM_ID_1"))
    assert edit_album["name"] == edit_name
    assert edit_album['description'] == edit_desc
    assert edit_album["add_user"]== False
    assert edit_album["download_series"]== True
    assert edit_album["send_series"]== False
    assert edit_album["delete_series"]== True
    assert edit_album["add_series"]== True
    assert edit_album["write_comments"]== True
    assert edit_album["notification_new_series"]== True
    assert edit_album["notification_new_comment"]==True

def test_add_user_in_album():
    album_shared_in_album = False
    album_added_in_album = False
    album_id_shared = env.env_var.get("ALBUM_ID_1")
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    #add an album 
    album_added = rq_album.create(token=env.env_var['USER_2_TOKEN'], data={"name":"my album"})
    #test if user2 contain album_id
    list_albums_user2= rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"),count=2)
    for album in list_albums_user2:
        if album['album_id']==album_id_shared:
            album_shared_in_album = True
        elif album['album_id']==album_added['album_id']:
            album_added_in_album = True    
    assert album_shared_in_album
    assert album_added_in_album 

################PERMISSION USER TEST################
def test_edit_album_forbidden():
    data = {"name":"edit name","description":"edit desc","sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_ID_1"), data=data,  status_code=403)

def test_edit_album_notif_and_more_forbidden():
    data = {"name":"edit name","description":"edit desc","addUser":True, "downloadSeries":False, "sendSeries":False, "deleteSeries":True, "addSeries":False, "writeComments":False, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_ID_1"), data=data,  status_code=403)
    
def test_edit_album_notif_ok():
    data = {"notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(token=env.env_var.get("USER_2_TOKEN"), album_id=env.env_var.get("ALBUM_ID_1"), data=data)

def test_remove_user_in_album():
    album_id_shared=env.env_var.get("ALBUM_ID_1")
    album_shared_in_album= True
    rq_album.remove_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    list_albums_user2= rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"),count=1)
    #check that the album is no longer present in its list 
    for album in list_albums_user2:
        if album['album_id']==album_id_shared:
            album_shared_in_album = False
    assert album_shared_in_album

def test_user_self_deletes_from_the_album():
    #re adding a user2 in the album
    album_id_shared = env.env_var.get("ALBUM_ID_1")
    album_shared_in_album= True
    rq_album.add_user(token=env.env_var.get("USER_1_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    rq_album.remove_user(token=env.env_var.get("USER_2_TOKEN"), album_id=album_id_shared, user_id=env.env_var.get("USER_2_MAIL"))
    list_albums_user2= rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"),count=1)
    #check that the album is no longer present in its list 
    for album in list_albums_user2:
        if album['album_id']==album_id_shared:
            
            album_shared_in_album = False
    assert album_shared_in_album

###################FILTER TEST#################################
def test_get_album_list_filter_by_name():    
    name_filter="re edit name"
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"name":name_filter}, count=1)
    assert list_albums[0]['name'] == name_filter

    #Test with same name
    name_filter="filter by name"
    album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":name_filter, "description": "a desc"})
    env.env_var["ALBUM_ID_5"]=album["album_id"]
    list_of_2_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"name":name_filter}, count=1)
    assert list_of_2_albums[0]['name'] == name_filter

    #Test bad request
    name_filter_false = "na"
    rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"name":name_filter_false}, count=0)


def test_get_album_list_filter_by_name_starts_with_star():    
    name_filter="*me"
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"name":name_filter}, count=2)
    assert list_albums[0]['name'] == "filter by name"
    assert list_albums[1]['name'] == "re edit name"
    assert list_albums[0]['album_id'] == env.env_var["ALBUM_ID_5"]
    assert list_albums[1]['album_id'] == env.env_var["ALBUM_ID_1"]

def test_get_album_list_filter_by_name_ends_with_star():    
    name_filter="a new*"
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"name":name_filter}, count=3)
    assert list_albums[0]['name'] == "a new album2"
    assert list_albums[1]['name'] == "a new album1"
    assert list_albums[2]['name'] == "a new album"
    assert list_albums[0]['album_id'] == env.env_var["ALBUM_ID_4"]
    assert list_albums[1]['album_id'] == env.env_var["ALBUM_ID_3"]
    assert list_albums[2]['album_id'] == env.env_var["ALBUM_ID_2"]

def test_get_album_list_filter_by_fuzzymatching():
    params={"name":"aaa new lfummn", "fuzzymatching":True}
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=3)
    assert list_albums[0]['name'] == "a new album2"
    assert list_albums[1]['name'] == "a new album1"
    assert list_albums[2]['name'] == "a new album"
    assert list_albums[0]['album_id'] == env.env_var["ALBUM_ID_4"]
    assert list_albums[1]['album_id'] == env.env_var["ALBUM_ID_3"]
    assert list_albums[2]['album_id'] == env.env_var["ALBUM_ID_2"]

def test_get_album_list_filter_by_favorite():
    params={"favorite":True}
    rq_album.add_favorite(env.env_var.get("USER_1_TOKEN"), env.env_var["ALBUM_ID_4"])
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)
    assert list_albums[0]["album_id"] == env.env_var['ALBUM_ID_4']


def test_get_album_list_filter_by_limit_offset():
    params={"offset":"2", "limit":"4"}
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=5)
    list_albums_with_params = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=5)
    assert list_albums[2] == list_albums_with_params[0]
    assert list_albums[3] == list_albums_with_params[1]

    params={"offset":"2"}
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=5)
    list_albums_with_params = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=5)
    assert list_albums[2] == list_albums_with_params[0]
    assert list_albums[3] == list_albums_with_params[1]
    assert list_albums[4] == list_albums_with_params[2]

    params={"limit":"4"}
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={}, count=5)
    list_albums_with_params = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=5)
    assert list_albums[0] == list_albums_with_params[0]
    assert list_albums[1] == list_albums_with_params[1]
    assert list_albums[2] == list_albums_with_params[2]
    assert list_albums[3] == list_albums_with_params[3]

def test_get_album_list_filter_by_limit_offset_bad_params():
    rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"limit":"a4"}, status_code=400)
    rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"limit":"-2"}, status_code=400)
    rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"limit":"/hfgh"}, status_code=400)

def test_get_album_list_sort_by_name():
    #sort +
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"sort":"name"}, count=5)
    assert list_albums[0]['name'] == "a new album"
    assert list_albums[1]['name'] == "a new album1"
    assert list_albums[2]['name'] == "a new album2"
    assert list_albums[3]['name'] == "filter by name"
    assert list_albums[4]['name'] == "re edit name"
    #sort -
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"sort":"-name"}, count=5)
    assert list_albums[4]['name'] == "a new album"
    assert list_albums[3]['name'] == "a new album1"
    assert list_albums[2]['name'] == "a new album2"
    assert list_albums[1]['name'] == "filter by name"
    assert list_albums[0]['name'] == "re edit name"

def test_get_album_list_by_created_time():
    #sort +
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"sort":"created_time"}, count=5)
    assert list_albums[0]['name'] == "re edit name"
    assert list_albums[1]['name'] == "a new album"
    assert list_albums[2]['name'] == "a new album1"
    assert list_albums[3]['name'] == "a new album2"
    assert list_albums[4]['name'] == "filter by name"
    #sort -
    list_albums = rq_album.get_list(token=env.env_var.get("USER_1_TOKEN"), params={"sort":"-created_time"}, count=5)
    assert list_albums[0]['name'] == "filter by name"
    assert list_albums[1]['name'] == "a new album2"
    assert list_albums[2]['name'] == "a new album1"
    assert list_albums[3]['name'] == "a new album"
    assert list_albums[4]['name'] == "re edit name"

##############################TEST DELETE######################################
def test_delete_album_not_found():
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id="1", status_code=404)

def test_delete_albums():
    #delete use 1 albums
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_1'], status_code=204)
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_2'], status_code=204)
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_3'], status_code=204)
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_4'], status_code=204)
    rq_album.delete(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var['ALBUM_ID_5'], status_code=204)
    #delete user 2 albums
    list_albums= rq_album.get_list(token=env.env_var.get("USER_2_TOKEN"), count=1)
    rq_album.delete(token=env.env_var.get("USER_2_TOKEN"), album_id=list_albums[0]["album_id"], status_code=204)
