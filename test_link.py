import rq_album
import env
import util
import random
import string
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

######################### TEST #############################
def test_get_usertoken():
    data = {"title":"karnak token read write", "scope_type":"user"}
    new_token = rq_capability_token.create(token=env.env_var['USER_1_TOKEN'], data=data)
    env.env_var["USER_TOKEN"]=new_token["secret"]
    
def test_stow():
    rq_studies.stow(token=env.env_var.get("USER_1_TOKEN"), link=True)



##############################TEST DELETE######################################

def test_clean_all_inbox():
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_1_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_2_TOKEN'])
    rq_studies.delete_all_from_inbox(token=env.env_var['USER_3_TOKEN'])
