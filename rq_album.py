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

def get_list(token, params={}, status_code=200, count=1):
    print()
    request_url = env.env_var.get("URL") + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    assert response.status_code == status_code
    if status_code == 200:
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

def delete_all(token):
    print()
    request_url = env.env_var.get("URL") + "/albums"
    headers = {"Authorization": "Bearer "+ token, "Accept": "application/json"}
    response = requests.get(request_url, headers=headers, params={})
    util.print_request("GET", response, request_url)
    if response.status_code == 200:
        list_albums = json.loads(response.content)
        for album in list_albums:
            #test if admin in album before delete
            delete(token, album['album_id']) 
            #if not in album, leave album (group)


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