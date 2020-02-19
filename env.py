
import os

__TRAVIS_URL="http://localhost:8042/api"
__TEST2_URL="http://localhost:8042/api"
#__TEST2_URL="https://test.kheops.online/api"
#__TEST2_URL="http://172.17.50.92:8042/api"
#__TEST2_URL="http://localhost:7575"
__STUDY_UID = "2.16.840.1.113669.632.20.1211.10000314223"
__SERIES_UID = "1.3.12.2.1107.5.1.4.48545.30000006100307470634300004693"
__PRINT_INFO = False

def initialize():
    global env_var
    env_var = {}
    if "TRAVIS" in os.environ:
        env_var["URL"] = __TRAVIS_URL
    else:
        env_var["URL"] = __TEST2_URL
    env_var["SERIES_UID"] = __SERIES_UID
    env_var["STUDY_UID"] = __STUDY_UID
    env_var["PRINT_INFO"] = __PRINT_INFO
    env_var["USER_1_MAIL"] = "titi@gmail.com"
    env_var["USER_2_MAIL"] = "toto@gmail.com"
    env_var["USER_3_MAIL"] = "tata@gmail.com"
