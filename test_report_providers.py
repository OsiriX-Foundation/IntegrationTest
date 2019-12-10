import requests
from requests.auth import AuthBase
import json
import urllib
import pytest
import env
import util


def test_init():
    env.initialize()
    print()

def test_get_token():
    print()
    token = util.get_token(username="titi", password="titi")
    env.env_var["USER_1_TOKEN"] = token
    token = util.get_token(username="toto", password="toto")
    env.env_var["USER_2_TOKEN"] = token
    token = util.get_token(username="tata", password="tata")
    env.env_var["USER_3_TOKEN"] = token

def test_new_album():
    print()
    album=util.new_album(token=env.env_var.get("USER_1_TOKEN"))
    env.env_var["ALBUM_ID"]=album["album_id"]

def test_stow():
    print()
    params = {"album": env.env_var.get("ALBUM_ID")}
    util.stow(token=env.env_var.get("USER_1_TOKEN"), params=params)

def test_album_studies_list():
    params = {"album": env.env_var.get("ALBUM_ID")}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)

def test_get_report_provider_list_empty():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), count=0)

def test_add_report_provider_1():
    name = "report provider name"
    url = "https://reportprovider.kheops.online/.well-known/kheops-report-configuration"
    data = {"name": name, "url": url}
    rp = util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"))
    env.env_var["REPORT_PROVIDER_1"]=rp["client_id"]

def test_add_report_provider_400():
    name = "name"
    url = "https://reportprovider.kheops.online/.well-known/xxx"
    data = {"name": name, "url": url}
    util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"), status_code=400)

def test_get_report_provider_list_1():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"))

def test_add_report_provider_2():
    name = "report provider name"
    url = "https://reportprovider.kheops.online/.well-known/kheops-report-configuration"
    data = {"name": name, "url": url}
    rp = util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"))
    env.env_var["REPORT_PROVIDER_2"] = rp["client_id"]

def test_get_report_provider_list_2():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), count=2)

def test_add_report_provider_3():
    name = "report provider name"
    url = "https://reportprovider.kheops.online/.well-known/kheops-report-configuration"
    data = {"name": name, "url": url}
    rp = util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"))
    env.env_var["REPORT_PROVIDER_3"] = rp["client_id"]

def test_get_report_provider_list_3():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), count=3)

def test_get_report_provider_1():
    util.get_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_1"))

def test_get_report_provider_2():
    util.get_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_2"))

def test_get_report_provider_3():
    util.get_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_3"))

def test_get_report_provider_404_album():
    util.get_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID").lower(), client_id=env.env_var.get("REPORT_PROVIDER_3"), status_code=404)

def test_get_report_provider_404_client_id():
    util.get_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_3").lower(), status_code=404)

def test_delete_report_provider_1():
    util.delete_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_1"))

def test_get_report_provider_list_2_():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), count=2)

def test_delete_report_provider_2():
    util.delete_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_2"))

def test_get_report_provider_list_1_():
    util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"))

def test_delete_report_provider_404_album():
    util.delete_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID").lower(), client_id=env.env_var.get("REPORT_PROVIDER_3"), status_code=404)

def test_delete_report_provider_404_client_id():
    util.delete_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_3").lower(), status_code=404)

def test_edit_report_provider_name():
    name = "new name"
    data = {"name": name}
    rp = util.edit_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"), client_id=env.env_var.get("REPORT_PROVIDER_3"), data=data)
    assert rp["name"] == name

def test_edit_report_provider_name_404_album():
    name = "new name"
    data = {"name": name}
    util.edit_report_provider(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID").lower(), client_id=env.env_var.get("REPORT_PROVIDER_2"), data=data, status_code=404)

def test_metadata_report_provider_valid():
    metadata = util.test_report_provider_uri(token=env.env_var.get("USER_1_TOKEN"), url="https://reportprovider.kheops.online/.well-known/kheops-report-configuration")
    assert metadata["valid"] == True

def test_metadata_report_provider_unvalid():
    metadata = util.test_report_provider_uri(token=env.env_var.get("USER_1_TOKEN"), url="https://reportprovider.kheops.online/.well-known/")
    assert metadata["valid"] == False

def test_delete_all_album():
    albums = util.list_albums(token=env.env_var.get("USER_1_TOKEN"))
    for album in albums:
        if album["number_of_users"] == 1:
            util.delete_album(token=env.env_var.get("USER_1_TOKEN"), album_id=album["album_id"])
