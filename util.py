import os
import requests
import numpy
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
    json.dumps(json_object, indent=4, sort_keys=True)


def stow(token, status_code = 200, file_name = "testStudy.dcm", params = {}):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    print_request("POST", response, request_url)
    assert response.status_code == status_code

def studies_list(token, params={}, count=1):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    if count != 0:
        assert response.status_code == 200
        assert response.headers.get("X-Total-Count") == str(count)
        studiesList = json.loads(response.content)
        return studiesList
    else:
        assert response.status_code == 204
        assert response.headers.get("X-Total-Count") == str(count)


def get_token(username, password, realm="travis", client_id="loginConnect"):
    well_known_url = "https://keycloak.kheops.online/auth/realms/"+str(realm)+"/.well-known/openid-configuration"
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
# CAPABILITIES TOKENS
################################################################

def new_token(token, data, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/capabilities"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        reportprovider = json.loads(response.content)
        return reportprovider


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


################################################################
# WEBHOOKS
################################################################

def new_webhook(token, album_id, data, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    data_tmp = data.copy()
    if "event" in data_tmp: del data_tmp["event"]
    encoded_data = urlencode(data_tmp)

    if "event" in data:
        events = data["event"]
        encoded_events = "".join(map(lambda e:"&event=" + str(e), events))
        encoded_data = encoded_data + encoded_events

    if encoded_data.startswith("&"):
        encoded_data = encoded_data[1:]

    response = requests.post(request_url, headers=headers, data=encoded_data)
    print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        webhook = json.loads(response.content)
        return webhook

def edit_webhook(token, album_id, webhook_id, data, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    data_tmp = data.copy()
    if "event" in data_tmp: del data_tmp["event"]
    if "add_event" in data_tmp: del data_tmp["add_event"]
    if "remove_event" in data_tmp: del data_tmp["remove_event"]
    encoded_data = urlencode(data_tmp)

    if "event" in data:
        events = data["event"]
        encoded_events = "".join(map(lambda e:"&event=" + str(e), events))
        encoded_data = encoded_data + encoded_events

    if "add_event" in data:
        add_events = data["add_event"]
        encoded_add_events = "".join(map(lambda e:"&add_event=" + e, add_events))
        encoded_data = encoded_data + encoded_add_events

    if "remove_event" in data:
        remove_events = data["remove_event"]
        encoded_remove_events = "".join(map(lambda e:"&remove_event=" + e, remove_events))
        encoded_data = encoded_data + encoded_remove_events

    if encoded_data.startswith("&"):
        encoded_data = encoded_data[1:]

    response = requests.patch(request_url, headers=headers, data=encoded_data)
    print_request("PATCH", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhook = json.loads(response.content)
        return webhook

def remove_webhook(token, album_id, webhook_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def get_webhook(token, album_id, webhook_id, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers)
    print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhook = json.loads(response.content)
        return webhook

def trigger_user_webhook(token, album_id, webhook_id, user_id, status_code=202):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id) + "/trigger"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"event":"new_user", "user":user_id}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code

def trigger_series_webhook(token, album_id, webhook_id, series_UID, study_UID, status_code=202):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id) + "/trigger"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"event":"new_series", "SeriesInstanceUID":series_UID, "StudyInstanceUID":study_UID}
    response = requests.post(request_url, headers=headers, data=urlencode(data))
    print_request("POST", response, request_url)
    assert response.status_code == status_code

def get_webhooks(token, album_id, limit=9999, offset=0, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks"
    headers = {"Authorization": "Bearer "+ token}
    params={"limit":limit, "offset":offset}
    response = requests.get(request_url, headers=headers, params=params)
    print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhooks = json.loads(response.content)
        return webhooks
