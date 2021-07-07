import util
import json
import env
import requests


################################################################
# STUDIES
################################################################
def get_list(token, params={}, count=-1):
    print()
    request_url = env.env_var.get("URL") + "/studies"
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(request_url, headers=headers, params=params)
    util.print_request("GET", response, request_url)
    if count > 0:
        assert response.status_code == 200
        assert response.headers.get("X-Total-Count") == str(count)
        studiesList = json.loads(response.content)
        return studiesList
    elif count == 0:
        assert response.status_code == 204
        assert response.headers.get("X-Total-Count") == str(count)
    else:
        assert response.status_code == 200 or 204
        if int(response.headers.get("X-Total-Count")) != 0:
            studiesList = json.loads(response.content)
            return studiesList


def stow(token, file_name="series/test1.dcm", params={}, status_code=200, link=False):
    print()
    if link:
        request_url = env.env_var.get("URL") + "/link/" + token + "/studies"
        headers = {"Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    else:
        request_url = env.env_var.get("URL") + "/studies"
        headers = {"Authorization": "Bearer " + token,
                   "Content-Type": "multipart/related; type=\"application/dicom\"; boundary=myboundary"}
    files = {'file': open(file_name, 'rb')}
    response = requests.post(request_url, headers=headers, files=files, params=params)
    util.print_request("POST", response, request_url)
    assert response.status_code == status_code


def add_in_album(token, params, study_instance_uid, album_id_dest, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + study_instance_uid + "/albums/" + album_id_dest
    if ("album" in params and "inbox" in params):
        assert False  # no permission
    elif ("album" in params):
        request_url += "?album=" + params["album"]
    elif ("inbox" in params):
        request_url += "?inbox=" + str(params["inbox"])

    headers = {"Authorization": "Bearer " + token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code


def add_in_inbox(token, study_instance_uid, album_id, status_code=201):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + study_instance_uid + "?album=" + album_id

    headers = {"Authorization": "Bearer " + token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)
    assert response.status_code == status_code


def delete_all_from_inbox(token):
    studies_list = get_list(token)
    if studies_list is not None:
        for study in studies_list:
            util.delete_study_from_inbox(token=token, studies_UID=study['0020000D']['Value'][0])


# TODO: Add option for inbox
def add_favorite_from_album(token, params, study_uid, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + study_uid + "/favorites"

    if "album" in params and "inbox" in params:
        assert False  # no permission
    elif "album" in params:
        request_url += "?album=" + params["album"]
    elif "inbox" in params:
        request_url += "?inbox=" + str(params["inbox"])

    headers = {"Authorization": "Bearer " + token}
    response = requests.put(request_url, headers=headers)
    util.print_request("PUT", response, request_url)

    assert response.status_code == status_code


def remove_favorite_from_album(token, study_UID, album, status_code=204):
    print()
    request_url = env.env_var.get("URL") + "/studies/" + study_UID + "/favorites?album=" + album
    headers = {"Authorization": "Bearer " + token}
    response = requests.delete(request_url, headers=headers)

    util.print_request("DELETE", response, request_url)
    assert response.status_code == status_code

# TODO: Clean after every test
