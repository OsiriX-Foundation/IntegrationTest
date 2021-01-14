import os
import requests
from requests.auth import AuthBase
import json
import urllib
from threading import Thread
import time
import pytest
import env


def print_request(methode, response, url):
    print("\t" + methode + " " + url + " ["+ str(response.status_code) + " " + requests.status_codes._codes[response.status_code][0].upper() + ", " + str(int(response.elapsed.total_seconds()*1000))+"ms]")
    print_info(response.content)

def urlencode(data):
    return urllib.parse.urlencode(data)

def print_info(info):
    if env.env_var.get("PRINT_INFO"):
        print(info)

def print_json(json_object):
    print(json.dumps(json_object, indent=4, sort_keys=True))

def add_user_keycloak(admin_username, admin_password, user_name, user_firstname, user_mail, user_username, user_password):

    well_known_url = env.env_var.get("KEYCLOAK_URL") + "/auth/realms/master" + "/.well-known/openid-configuration"
    response = requests.get(well_known_url)
    assert response.status_code == 200
    well_known = json.loads(response.content)
    assert "token_endpoint" in well_known

    token_endpoint = well_known["token_endpoint"]

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "password", "username": admin_username, "password": admin_password, "client_id":"admin-cli"}
    response = requests.post(token_endpoint, headers=headers, data=data)
    token_response = json.loads(response.content)
    admin_token = token_response["access_token"]
    
    create_user_url = env.env_var.get("KEYCLOAK_URL") +"/auth/admin/realms/"+ env.env_var.get("KEYCLOAK_REALM") + "/users"
    headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer " + admin_token}
    data = {"enabled":True, "attributes":{}, "username":user_username, "emailVerified":True,"email":user_mail, "firstName":user_firstname, "lastName":user_name}
    data = json.dumps(data)
    response = requests.post(create_user_url, headers=headers, data=data)
    assert response.status_code == 201 or 409

    if "Location" in response.headers.keys():
        reset_password_url = response.headers["Location"] + "/reset-password"
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer " + admin_token}
        data = {"type":"password", "value":user_password, "temporary":False}
        data = json.dumps(data)
        response = requests.put(reset_password_url, headers=headers, data=data)
        assert response.status_code == 204
    else:
        print("user already exist")
        print(response.content)
        

def get_token(username, password, client_id="loginConnect"):
    well_known_url = env.env_var.get("KEYCLOAK_URL") + "/auth/realms/" + env.env_var.get("KEYCLOAK_REALM") + "/.well-known/openid-configuration"
    response = requests.get(well_known_url)
    assert response.status_code == 200
    well_known = json.loads(response.content)
    assert "token_endpoint" in well_known

    token_endpoint = well_known["token_endpoint"]

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "password", "username": username, "password": password, "client_id":client_id}
    response = requests.post(token_endpoint, headers=headers, data=data)
    token_response = json.loads(response.content)
    return token_response["access_token"]

def register(token):
    request_url = env.env_var.get("URL") + "/register"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"access_token": token}
    response = requests.post(request_url, headers=headers, data=data)
    token_response = json.loads(response.content)
    return token_response

################################################################
# REPORT PROVIDER
################################################################

def new_report_provider(token, data, album_id, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums/"+str(album_id)+"/reportproviders"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        reportprovider = json.loads(response.content)
        return reportprovider

def test_report_provider_uri(token, url):
    print()
    request_url = env.env_var.get("URL") + "/reportproviders/metadata"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"url": url}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == 200
    metadata = json.loads(response.content)
    return metadata

def get_report_provider(token, client_id, album_id, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/reportproviders/" + str(client_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers)
    print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        reportprovider = json.loads(response.content)
        return reportprovider

def report_provider_list(token, album_id, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/albums/"+str(album_id)+"/reportproviders"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    assert response.status_code == 200
    assert response.headers.get("X-Total-Count") == str(count)
    report_providers = json.loads(response.content)
    return report_providers

def edit_report_provider(token, client_id, album_id, data, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/reportproviders/" + str(client_id)
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.patch(request_url, headers=headers, data=urlencode(data))
    print_request("PATCH", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        reportprovider = json.loads(response.content)
        return reportprovider

def delete_report_provider(token, client_id, album_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/reportproviders/" + str(client_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    print_request("DELETE", response, request_url)
    assert response.status_code == status_code


################################################################
# SERIES & STUDIES
################################################################

def share_series_in_album(token, studies_UID, series_UID, album_id, X_Authorization_Source = "", status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/series/"+series_UID+"/albums/"+album_id
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    if X_Authorization_Source != "":
        headers["X-Authorization-Source"] = "Bearer " + X_Authorization_Source
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def share_study_in_album(token, studies_UID, album_id, X_Authorization_Source = "", status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/albums/"+album_id
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    if X_Authorization_Source != "":
        headers["X-Authorization-Source"] = "Bearer " + X_Authorization_Source
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def share_study_in_album_from_album(token, studies_UID, album_src_id, album_dst_id, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + studies_UID + "/albums/" + album_dst_id
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    params = {"album": album_src_id}
    response = requests.put(request_url, headers=headers, params=params)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def share_series_with_user(token, user, studies_UID, series_UID, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/series/"+series_UID+"/users/"+user
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def share_study_with_user(token, user, studies_UID, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/users/"+user
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def delete_series_from_inbox(token, studies_UID, series_UID, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/series/"+series_UID
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def delete_study_from_inbox(token, studies_UID, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def delete_series_from_album(token, studies_UID, series_UID, album_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/series/"+series_UID+"/albums/"+album_id
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def appropriate_study(token, studies_UID, X_Authorization_Source = "", status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID
    headers = {"Authorization": "Bearer "+ token}
    if X_Authorization_Source != "":
        headers["X-Authorization-Source"] = "Bearer " + X_Authorization_Source
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code

def appropriate_series(token, studies_UID, series_UID, X_Authorization_Source = "", status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/"+studies_UID+"/series/"+series_UID
    headers = {"Authorization": "Bearer "+ token}
    if X_Authorization_Source != "":
        headers["X-Authorization-Source"] = "Bearer " + X_Authorization_Source
    response = requests.put(request_url, headers=headers)
    print_request("PUT", response, request_url)
    assert response.status_code == status_code
