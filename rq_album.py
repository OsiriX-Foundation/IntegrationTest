import os
import util
from requests.auth import AuthBase
import json
import env
import requests
import sys

################################################################
# ALBUMS
################################################################
def create(token, data={"name":"a name"}, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        album = json.loads(response.content)
        return album

def edit(token, album_id, data, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.patch(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("PATCH", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        album = json.loads(response.content)
        return album

def get_list(token, params={}, status_code=200, count=-1):
    print()
    request_url = env.env_var.get("URL") + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        if count != -1:
            assert response.headers.get("X-Total-Count") == str(count)
        albums = json.loads(response.content)
        return albums

def get(token, album_id, params={}, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        album = json.loads(response.content)
        return album

def delete(token, album_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def delete_all(token, user_id):
    print()
    list_albums = get_list(token=token)
    for album in list_albums:

        if album['is_admin'] == True:
            delete(token, album['album_id']) 
        else:
            remove_user(token=token, album_id= album['album_id'], user_id=user_id)


#################REQUEST WITH USER################################
def add_user(token, album_id, user_id, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/users/" + user_id
    headers = {"Authorization": "Bearer "+ token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code

def get_list_of_user(token, album_id, count=1, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/users"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        assert response.headers.get("X-Total-Count") == str(count)
        albums = json.loads(response.content)
        return albums

def remove_user(token, album_id, user_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/users/" + user_id
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code

def upgrade_user_to_admin(token, album_id, user_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/users/" + user_id + "/admin"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code

def downgrade_admin_to_user(token, album_id, user_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/users/" + user_id + "/admin"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code


#################REQUEST WITH FAVORITE################################
def add_favorite(token, album_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/favorites/"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code
def remove_favorite(token, album_id, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/favorites"
    headers = {"Authorization": "Bearer "+ token}
    response = requests.delete(request_url, headers=headers)
    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code


#################REQUEST WITH COMMENT################################
def post_comment(token, album_id, data={"comment":"default comment"}, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/comments"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, headers=headers, data=util.urlencode(data))
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code
    if status_code == 201:
        album = json.loads(response.content)
        return album

def get_events(token, album_id, params={}, count=1, status_code=200):
    print()
    request_url = env.env_var.get("URL") + "/albums/" + album_id + "/events"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
        assert response.headers.get("X-Total-Count") == str(count)
        album = json.loads(response.content)
        return album
