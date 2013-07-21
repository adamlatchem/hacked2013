#!/usr/bin/env python
import json, httplib
import lightapi
api = lightapi.connect()
c.request('POST', '/api', json.dumps({"devicetype": "iPhone", "username": "1234567890"}))
result = json.loads(c.getresponse().read())
print result
