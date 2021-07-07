import env
import util

def test_init():
    env.initialize()
    print()
    
def test_register_in_keycloak():
    print()
    util.add_user_keycloak(admin_username="admin", admin_password="12345", user_name="titi", user_firstname="titi", user_mail="titi@gmail.com", user_username="titi", user_password="titi")
    util.add_user_keycloak(admin_username="admin", admin_password="12345", user_name="toto", user_firstname="toto", user_mail="toto@gmail.com", user_username="toto", user_password="toto")
    util.add_user_keycloak(admin_username="admin", admin_password="12345", user_name="tata", user_firstname="tata", user_mail="tata@gmail.com", user_username="tata", user_password="tata")
    util.add_user_keycloak(admin_username="admin", admin_password="12345", user_name="karnak", user_firstname="karnak", user_mail="karnak@gmail.com", user_username="karnak", user_password="karnak")


def test_get_token():
    print()
    token = util.get_token(username="titi@gmail.com", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto@gmail.com", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata@gmail.com", password="tata")
    env.env_var["USER_3_TOKEN"] = token

