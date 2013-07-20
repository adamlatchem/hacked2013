#!/usr/bin/env python
import json, httplib
c = httplib.HTTPConnection('192.168.2.208', 80)
c.connect()
c.request('POST', '/api', json.dumps({"devicetype": "iPhone", "username": "1234567890"}))
result = json.loads(c.getresponse().read())
print result
