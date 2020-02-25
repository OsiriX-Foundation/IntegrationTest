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
"""
def test_get_user_exist():
    users_list = rq_user.get(env.env_var["USER_1_TOKEN"], status_code=200, params={"reference":env.env_var["USER_1_MAIL"]})
"""