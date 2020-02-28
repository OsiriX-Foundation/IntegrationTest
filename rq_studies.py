import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys

################################################################
# STUDIES
################################################################
def get_list(token, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    if count != 0:
        assert response.status_code == 200
        assert response.headers.get("X-Total-Count") == str(count)
        studiesList = json.loads(response.content)
        return studiesList
    else:
        assert response.status_code == 204
        assert response.headers.get("X-Total-Count") == str(count)

def stow(token, file_name = "series/test1.dcm", params = {}, status_code = 200):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code

def add_in_album(token, params, study_instance_uid, album_id_dest, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + study_instance_uid + "/albums/" + album_id_dest
    if("album" in params and "inbox" in params):
        assert False #no permission
    elif("album" in params):
        request_url +="?album="+params["album"]
    elif("inbox" in params):
        request_url +="?inbox="+str(params["inbox"])
    
    headers = {"Authorization": "Bearer "+ token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code