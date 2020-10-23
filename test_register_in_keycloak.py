import env
import util

def test_init():
    env.initialize()
    print()
    
def test_register_in_keycloak():
    print()
    util.add_user_keycloak(admin_username="admin", admin_password="admin", user_name="titi", user_firstname="titi", user_mail="titi@gmail.com", user_username="titi", user_password="titi")
    util.add_user_keycloak(admin_username="admin", admin_password="admin", user_name="toto", user_firstname="toto", user_mail="toto@gmail.com", user_username="toto", user_password="toto")
    util.add_user_keycloak(admin_username="admin", admin_password="admin", user_name="tata", user_firstname="tata", user_mail="tata@gmail.com", user_username="tata", user_password="tata")


def test_get_token():
    print()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

