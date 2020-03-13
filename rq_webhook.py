import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys

################################################################
# WEBHOOKS
################################################################

def create(token, album_id, data, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    data_tmp = data.copy()
    if "event" in data_tmp: del data_tmp["event"]
    encoded_data = util.urlencode(data_tmp)

    if "event" in data:
        events = data["event"]
        encoded_events = "".join(map(lambda e:"&event=" + str(e), events))
        encoded_data = encoded_data + encoded_events

    if encoded_data.startswith("&"):
        encoded_data = encoded_data[1:]

    response = requests.post(request_url, headers=headers, data=encoded_data)
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        webhook = json.loads(response.content)
        return webhook

def edit(token, album_id, webhook_id, data, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    data_tmp = data.copy()
    if "event" in data_tmp: del data_tmp["event"]
    if "add_event" in data_tmp: del data_tmp["add_event"]
    if "remove_event" in data_tmp: del data_tmp["remove_event"]
    encoded_data = util.urlencode(data_tmp)

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
    util.print_request("PATCH", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhook = json.loads(response.content)
        return webhook

def remove(token, album_id, webhook_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def get(token, album_id, webhook_id, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id)
    headers = {"Authorization": "Bearer "+ token}
    response = requests.get(request_url, headers=headers)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhook = json.loads(response.content)
        return webhook

def trigger_user(token, album_id, webhook_id, user_id, status_code=202):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id) + "/trigger"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"event":"new_user", "user":user_id}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code

def trigger_series(token, album_id, webhook_id, series_UID, study_UID, status_code=202):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks/" + str(webhook_id) + "/trigger"
    headers = {"Authorization": "Bearer "+ token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"event":"new_series", "SeriesInstanceUID":series_UID, "StudyInstanceUID":study_UID}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code

def get_list(token, album_id, limit=9999, offset=0, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + str(album_id) + "/webhooks"
    headers = {"Authorization": "Bearer "+ token}
    params={"limit":limit, "offset":offset}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        webhooks = json.loads(response.content)
        return webhooks
