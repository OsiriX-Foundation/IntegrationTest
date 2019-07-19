
import os

__TRAVIS_URL="http://localhost:8042/api"
__TEST2_URL="https://test2.kheops.online/api"
#__URL="http://172.17.20.103:8042/api"
__USER_1_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJhdXRob3JpemF0aW9uLmtoZW9wcy5vbmxpbmUiLCJzdWIiOiJjMmZkMGI2Ni1kYWM0LTRiOTgtOTM0MS1kNGYzYjMwM2JkNGUiLCJlbWFpbCI6InRpdGlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MjUyMjk0MzU3MiwiaXNzIjoiYXV0aG9yaXphdGlvbi5raGVvcHMub25saW5lIiwiaWF0IjoxNTIyOTM5OTcyfQ.hrau4sW3iVf_mS0gLiO_uulMrNUTe_D9FRKfK6AtK48"
__STUDY_UID = "2.16.840.1.113669.632.20.1211.10000314223"
__SERIES_UID = "1.3.12.2.1107.5.1.4.48545.30000006100307470634300004693"
__PRINT_INFO = False

def initialize():
    global URL
    if "TRAVIS" in os.environ:
        URL = __TRAVIS_URL
    else:
        URL = __TEST2_URL
    global USER_1_TOKEN
    USER_1_TOKEN = __USER_1_TOKEN
    global SERIES_UID
    SERIES_UID = __SERIES_UID
    global STUDY_UID
    STUDY_UID = __STUDY_UID
    global PRINT_INFO
    PRINT_INFO = __PRINT_INFO
