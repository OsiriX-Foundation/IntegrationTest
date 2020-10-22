
import os

__TRAVIS_URL="http://localhost:8042/api"
__TRAVIS_KEYCLOAK_URL="https://keycloak.kheops.online/auth/realms/"
__TRAVIS_KEYCLOAK_REALM="travis"
#__TEST2_URL="http://localhost:8042/api"
#__TEST2_URL="https://test.kheops.online/api"
#__TEST2_URL="http://192.168.67.221:8042/api"
#__TEST2_URL="http://localhost:7575"
__TEST2_URL="http://localhost:80/api"
__KEYCLOAK_URL="http://localhost:8080/auth/realms/"
__KEYCLOAK_REALM="travis"
__KEYCLOAK_REALM="kheops"
__STUDY_UID = "2.16.840.1.113669.632.20.1211.10000314223"
__SERIES_UID = "1.3.12.2.1107.5.1.4.48545.30000006100307470634300004693"
__PRINT_INFO = False


__STUDY_UID1 = "2.16.840.1.113669.632.20.1211.10000314223"
__SERIES_UID1 = "1.3.12.2.1107.5.1.4.48545.30000006100307470634300004693"

__STUDY_UID2 = "2.16.840.1.113669.632.20.1211.10000231621"
__SERIES_UID2 = "1.3.12.2.1107.5.1.4.54693.30000006053107175587500014744"

__STUDY_UID3 = "2.16.840.1.113669.632.20.1211.10000307912"
__SERIES_UID3 = "1.3.6.1.4.1.19291.2.1.2.13214421782916617324360484294967295589745577"

__STUDY_UID4 = "2.16.840.1.113669.632.20.1211.10000329900"
__SERIES_UID4 = "1.3.12.2.1107.5.1.4.54693.30000006102508593206200000003"

__STUDY_UID4_1 = "2.16.840.1.113669.632.20.1211.10000329900"
__SERIES_UID4_1 = "1.3.12.2.1107.5.1.4.54693.30000006102508593206200000015"

__STUDY_UID5 = "1.2.840.113745.101000.1008000.38446.6272.7138759"
__SERIES_UID5 = "1.3.12.2.1107.5.2.13.20561.30000005042216091690600001946"



def initialize():
    global env_var
    env_var = {}
    if "TRAVIS" in os.environ:
        env_var["URL"] = __TRAVIS_URL
        env_var["KEYCLOAK_URL"] = __TRAVIS_KEYCLOAK_URL
        env_var["KEYCLOAK_REALM"] = __TRAVIS_KEYCLOAK_REALM
    else:
        env_var["URL"] = __TEST2_URL
        env_var["KEYCLOAK_URL"] = __KEYCLOAK_URL
        env_var["KEYCLOAK_REALM"] = __KEYCLOAK_REALM

    env_var["STUDY_UID"] = __STUDY_UID
    env_var["SERIES_UID"] = __SERIES_UID

    env_var["STUDY_UID1"] = __STUDY_UID1
    env_var["SERIES_UID1"] = __SERIES_UID1

    env_var["STUDY_UID2"] = __STUDY_UID2
    env_var["SERIES_UID2"] = __SERIES_UID2

    env_var["STUDY_UID3"] = __STUDY_UID3
    env_var["SERIES_UID3"] = __SERIES_UID3

    env_var["STUDY_UID4"] = __STUDY_UID4
    env_var["SERIES_UID4"] = __SERIES_UID4

    env_var["STUDY_UID4_1"] = __STUDY_UID4_1
    env_var["SERIES_UID4_1"] = __SERIES_UID4_1

    env_var["STUDY_UID5"] = __STUDY_UID5
    env_var["SERIES_UID5"] = __SERIES_UID5

    env_var["PRINT_INFO"] = __PRINT_INFO
    env_var["USER_1_MAIL"] = "titi@gmail.com"
    env_var["USER_2_MAIL"] = "toto@gmail.com"
    env_var["USER_3_MAIL"] = "tata@gmail.com"
    env_var["USER_KARNAK_MAIL"] = "karnak@gmail.com"
