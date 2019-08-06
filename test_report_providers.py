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

def test_stow():
    print()
    util.stow(token=env.env_var.get("USER_1_TOKEN"))

def test_studies_list():
    params = {"inbox": "True"}
    util.studies_list(token=env.env_var.get("USER_1_TOKEN"), params=params, count=1)
