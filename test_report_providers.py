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
import util



def test_new_album():
    env.initialize()
    print()
    album=util.new_album(token=env.USER_1_TOKEN)

def test_stow():
    env.initialize()
    print()
    util.stow(token=env.USER_1_TOKEN)

def test_studies_list():
    env.initialize()
    params = {"inbox": "True"}
    util.studies_list(token=env.USER_1_TOKEN, params=params, count=1)
