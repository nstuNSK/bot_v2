#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import time
import json
import sys
import requests
import database as data
import getter
import base64

token = getter.get_token()
vk = vk_api.VkApi(token=token)
r = read()
print(r)
vk._auth_token()
WAIT_FILLING_POINTS = "-3"
WAIT_FILLING = "-2"
TEMP_FILLING = "-1"


