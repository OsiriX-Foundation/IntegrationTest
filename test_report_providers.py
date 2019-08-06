import requests
from requests.auth import AuthBase
import json
import urllib
import pytest
import env
import util


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

def test_add_report_provider():
    name = "report provider name"
    url = "https://reportprovider.kheops.online/.well-known/kheops-report-configuration"
    data = {"name": name, "url": url}
    util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"))

def test_add_report_provider_400():
    name = "name"
    url = "https://reportprovider.kheops.online/.well-known/xxx"
    data = {"name": name, "url": url}
    util.new_report_provider(token=env.env_var.get("USER_1_TOKEN"), data=data, album_id=env.env_var.get("ALBUM_ID"), status_code=400)

def test_get_report_provider_list():
    rp = util.report_provider_list(token=env.env_var.get("USER_1_TOKEN"), album_id=env.env_var.get("ALBUM_ID"))
