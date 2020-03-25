import rq_album
import rq_user
import env
import util
import random
import string
import json
import rq_studies

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

def test_register():
    util.register(token=env.env_var['USER_1_TOKEN'])
    util.register(token=env.env_var['USER_2_TOKEN'])
    util.register(token=env.env_var['USER_3_TOKEN'])

def test_get_events_mutation_when_create_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])

    data = {"name":"ablum test comment", "description":"desc test album comment"}
    new_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["ALBUM_ID_COMMENT"]=new_album["album_id"]
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=1, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "CREATE_ALBUM"
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[0]["origin"]["can_access"] == True

def test_post_comment_in_album():
    env.env_var["COMMENT_1"] = "first_comment"
    rq_album.post_comment(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], data={"comment":env.env_var["COMMENT_1"] }, status_code=204)

def test_get_comment_in_album():
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=2, status_code=200)
    assert events_list[0]["event_type"] == "Comment"
    assert events_list[0]["comment"] == env.env_var["COMMENT_1"]
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[0]["origin"]["can_access"] == True
    assert events_list[1]["event_type"] == "Mutation"
    assert events_list[1]["mutation_type"] == "CREATE_ALBUM"
    assert events_list[1]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[1]["origin"]["can_access"] == True

def test_add_user_in_album_and_get_mutation():
    rq_album.add_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_COMMENT"], env.env_var["USER_2_MAIL"], status_code=201)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=3, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "ADD_USER"
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[0]["origin"]["can_access"] == True
    assert events_list[0]["target"]["email"] == env.env_var["USER_2_MAIL"]
    assert events_list[0]["target"]["can_access"] == True
    assert events_list[1]["event_type"] == "Comment"
    assert events_list[1]["comment"] == env.env_var["COMMENT_1"]
    assert events_list[2]["event_type"] == "Mutation"
    assert events_list[2]["mutation_type"] == "CREATE_ALBUM"

def test_edit_album_and_get_mutation():
    data_edit = {"name":"album comment edit","description":"edit album comment","sendSeries":True, "addUser":True, "deleteSeries":True, "notificationNewSeries":False, "notificationNewComment":False}
    rq_album.edit(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_COMMENT"], data_edit, status_code=200)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=4, status_code=200)
    assert events_list[0]["mutation_type"] == "EDIT_ALBUM"
    assert events_list[1]["mutation_type"] == "ADD_USER"
    assert events_list[1]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[1]["target"]["email"] == env.env_var["USER_2_MAIL"]
    assert events_list[2]["comment"] == env.env_var["COMMENT_1"]
    assert events_list[3]["mutation_type"] == "CREATE_ALBUM"

def test_other_user_in_album_post_comment():
    env.env_var["COMMENT_2"] = "second_comment"
    rq_album.post_comment(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], data={"comment":env.env_var["COMMENT_2"] }, status_code=204)

def test_get_comment_with_other_user_in_album():
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=5, status_code=200)
    assert events_list[0]["event_type"] == "Comment"
    assert events_list[0]["comment"] == env.env_var["COMMENT_2"]
    assert events_list[0]["origin"]["email"] == env.env_var["USER_2_MAIL"]
    assert events_list[0]["origin"]["can_access"] == True

def test_post_comment_with_other_user_that_not_in_album():
    rq_album.post_comment(env.env_var["USER_3_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], data={"comment":"other user not in album comment" }, status_code=404)


def test_remove_user_permission_to_write_comment():
    data_edit = {"name":"album comment edit","description":"edit album comment", "writeComments":False}
    rq_album.edit(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_COMMENT"], data_edit, status_code=200)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=6, status_code=200)
    assert events_list[0]["mutation_type"] == "EDIT_ALBUM"
    rq_album.post_comment(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], data={"comment":"other user not have permission" }, status_code=403)


def test_admin_have_permission_to_write_comment():
    env.env_var["COMMENT_3"] = "third_comment"
    rq_album.post_comment(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], data={"comment":env.env_var["COMMENT_3"] }, status_code=204)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'], count=7, status_code=200)
    assert events_list[0]["comment"] == env.env_var["COMMENT_3"]
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]

def test_get_comments_by_user():
    params={"types":"comments"}
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert events_list[0]["comment"] == env.env_var["COMMENT_3"]
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_2"]
    assert events_list[1]["origin"]["email"] == env.env_var["USER_2_MAIL"]
    assert events_list[2]["comment"] == env.env_var["COMMENT_1"]
    assert events_list[2]["origin"]["email"] == env.env_var["USER_1_MAIL"]

    events_list = rq_album.get_events(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert events_list[0]["comment"] == env.env_var["COMMENT_3"]
    assert events_list[0]["origin"]["email"] == env.env_var["USER_1_MAIL"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_2"]
    assert events_list[1]["origin"]["email"] == env.env_var["USER_2_MAIL"]
    assert events_list[2]["comment"] == env.env_var["COMMENT_1"]
    assert events_list[2]["origin"]["email"] == env.env_var["USER_1_MAIL"]

def test_get_comments_limit_by_user():
    limit = 2
    params={"types":"comments", "limit":limit}
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==limit
    assert events_list[0]["comment"] == env.env_var["COMMENT_3"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_2"]

    events_list = rq_album.get_events(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==limit
    assert events_list[0]["comment"] == env.env_var["COMMENT_3"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_2"]



def test_get_comments_offset_by_user():
    offset = 1
    params={"types":"comments", "offset":offset}
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==2
    assert events_list[0]["comment"] == env.env_var["COMMENT_2"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_1"]

    events_list = rq_album.get_events(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==2
    assert events_list[0]["comment"] == env.env_var["COMMENT_2"]
    assert events_list[1]["comment"] == env.env_var["COMMENT_1"]

def test_get_comments_offset_limit_by_user():
    offset = 1
    limit = 1
    params={"types":"comments", "offset":offset, "limit":limit}
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==1
    assert events_list[0]["comment"] == env.env_var["COMMENT_2"]

    events_list = rq_album.get_events(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_COMMENT'],params=params, count=3, status_code=200)
    assert len(events_list)==1
    assert events_list[0]["comment"] == env.env_var["COMMENT_2"]



def test_get_album_with_correct_response_in_function_of_number_comment():
    album_comment = rq_album.get(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_COMMENT"], params={}, status_code=200)
    assert album_comment["number_of_comments"] == 3
    assert album_comment["number_of_users"] == 2
    assert album_comment["album_id"] == env.env_var["ALBUM_ID_COMMENT"]


############################MUTATIONS#######################################

def test_mutation_create_album():

    mutation_album = rq_album.create(token=env.env_var['USER_1_TOKEN'], data={"name":"CREATE_ALBUM", "description":"create for mutation test"})
    env.env_var["ALBUM_ID_MUTATION"]=mutation_album["album_id"]
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=1, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "CREATE_ALBUM"
    assert len(events_list) == 1

def test_mutation_add_user_in_album():

    rq_album.add_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_MUTATION"], env.env_var["USER_2_MAIL"], status_code=201)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=2, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "ADD_USER"
    assert len(events_list) == 2


def test_mutation_user_leave_in_album():
    rq_album.remove_user(token=env.env_var["USER_2_TOKEN"], album_id=env.env_var['ALBUM_ID_MUTATION'], user_id=env.env_var.get("USER_2_MAIL"))
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=3, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "LEAVE_ALBUM"
    assert len(events_list) == 3


def test_mutation_add_and_upgrade_user_in_album():
    rq_album.upgrade_user_to_admin(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], env.env_var["USER_2_MAIL"], status_code=204)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=4, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "ADD_ADMIN"
    assert len(events_list) == 4

def test_mutation_downgrade_user_in_album():
    rq_album.downgrade_admin_to_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_MUTATION"], env.env_var["USER_2_MAIL"], status_code=204)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=5, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "DEMOTE_ADMIN"
    assert len(events_list) == 5

def test_mutation_upgrade_user_in_album():
    rq_album.upgrade_user_to_admin(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], env.env_var["USER_2_MAIL"], status_code=204)
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=6, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "PROMOTE_ADMIN"
    assert len(events_list) == 6

def test_mutation_admin_remove_user():
    rq_album.remove_user(token=env.env_var["USER_1_TOKEN"], album_id=env.env_var['ALBUM_ID_MUTATION'], user_id=env.env_var.get("USER_2_MAIL"))
    events_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], count=7, status_code=200)
    assert events_list[0]["event_type"] == "Mutation"
    assert events_list[0]["mutation_type"] == "REMOVE_USER"
    assert len(events_list) == 7

def test_post_comments_in_album_who_contain_mutation():
    rq_album.add_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_MUTATION"], env.env_var["USER_2_MAIL"], status_code=201)
    rq_album.add_user(env.env_var["USER_1_TOKEN"], env.env_var["ALBUM_ID_MUTATION"], env.env_var["USER_3_MAIL"], status_code=201)

    env.env_var["COMMENT_MUTATION_1"] = "first_comment"
    env.env_var["COMMENT_MUTATION_2"] = "second_comment"
    env.env_var["COMMENT_MUTATION_3"] = "third_comment"

    rq_album.post_comment(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], data={"comment":env.env_var["COMMENT_MUTATION_1"] }, status_code=204)
    rq_album.post_comment(env.env_var["USER_2_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], data={"comment":env.env_var["COMMENT_MUTATION_2"]}, status_code=204)
    rq_album.post_comment(env.env_var["USER_3_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], data={"comment":env.env_var["COMMENT_MUTATION_3"] }, status_code=204)

def test_get_all_comments():
    params={"types":"comments"}
    comments_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], params=params, count=3, status_code=200)
    assert comments_list[0]["comment"] == env.env_var["COMMENT_MUTATION_3"]
    assert comments_list[1]["comment"] == env.env_var["COMMENT_MUTATION_2"]
    assert comments_list[2]["comment"] == env.env_var["COMMENT_MUTATION_1"]


def test_get_all_mutations():
    params={"types":"mutations"}
    mutations_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], params=params, count=9, status_code=200)
    assert mutations_list[0]["mutation_type"] == "ADD_USER"
    assert mutations_list[1]["mutation_type"] == "ADD_USER"
    assert mutations_list[2]["mutation_type"] == "REMOVE_USER"
    assert mutations_list[3]["mutation_type"] == "PROMOTE_ADMIN"
    assert mutations_list[4]["mutation_type"] == "DEMOTE_ADMIN"
    assert mutations_list[5]["mutation_type"] == "ADD_ADMIN"
    assert mutations_list[6]["mutation_type"] == "LEAVE_ALBUM"
    assert mutations_list[7]["mutation_type"] == "ADD_USER"
    assert mutations_list[8]["mutation_type"] == "CREATE_ALBUM"


def test_get_all_comments_and_mutations_with_types():
    params={"types":["comments","mutations"]}
    mutations_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], params=params, count=12, status_code=200)
    assert mutations_list[0]["comment"] == env.env_var["COMMENT_MUTATION_3"]
    assert mutations_list[1]["comment"] == env.env_var["COMMENT_MUTATION_2"]
    assert mutations_list[2]["comment"] == env.env_var["COMMENT_MUTATION_1"]
    assert mutations_list[3]["mutation_type"] == "ADD_USER"
    assert mutations_list[4]["mutation_type"] == "ADD_USER"
    assert mutations_list[5]["mutation_type"] == "REMOVE_USER"
    assert mutations_list[6]["mutation_type"] == "PROMOTE_ADMIN"
    assert mutations_list[7]["mutation_type"] == "DEMOTE_ADMIN"
    assert mutations_list[8]["mutation_type"] == "ADD_ADMIN"
    assert mutations_list[9]["mutation_type"] == "LEAVE_ALBUM"
    assert mutations_list[10]["mutation_type"] == "ADD_USER"
    assert mutations_list[11]["mutation_type"] == "CREATE_ALBUM"

def test_get_all_comments_and_mutations_without_types():
    params={}
    mutations_list = rq_album.get_events(env.env_var["USER_1_TOKEN"], env.env_var['ALBUM_ID_MUTATION'], params=params, count=12, status_code=200)
    assert mutations_list[0]["comment"] == env.env_var["COMMENT_MUTATION_3"]
    assert mutations_list[1]["comment"] == env.env_var["COMMENT_MUTATION_2"]
    assert mutations_list[2]["comment"] == env.env_var["COMMENT_MUTATION_1"]
    assert mutations_list[3]["mutation_type"] == "ADD_USER"
    assert mutations_list[4]["mutation_type"] == "ADD_USER"
    assert mutations_list[5]["mutation_type"] == "REMOVE_USER"
    assert mutations_list[6]["mutation_type"] == "PROMOTE_ADMIN"
    assert mutations_list[7]["mutation_type"] == "DEMOTE_ADMIN"
    assert mutations_list[8]["mutation_type"] == "ADD_ADMIN"
    assert mutations_list[9]["mutation_type"] == "LEAVE_ALBUM"
    assert mutations_list[10]["mutation_type"] == "ADD_USER"
    assert mutations_list[11]["mutation_type"] == "CREATE_ALBUM"

def test_delete_all_album():
    rq_album.delete_all(token=env.env_var['USER_1_TOKEN'], user_id=env.env_var['USER_1_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_2_TOKEN'], user_id=env.env_var['USER_2_MAIL'])
    rq_album.delete_all(token=env.env_var['USER_3_TOKEN'], user_id=env.env_var['USER_3_MAIL'])

def test_clean_all_inbox():
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_2_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_3_TOKEN'])
