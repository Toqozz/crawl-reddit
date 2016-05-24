import sys
import json
import pycurl
from io import BytesIO

buffer = BytesIO()
curl = pycurl.Curl()
curl.setopt(curl.URL, "https://www.reddit.com/r/talesfromtechsupport.json")
curl.setopt(curl.USERAGENT, "/u/Toqoz")
curl.setopt(curl.WRITEDATA, buffer)
curl.setopt(curl.VERBOSE, True)
curl.perform()
curl.close()

body = buffer.getvalue().decode('utf-8')

response = json.loads(body)["data"]["children"][15]["data"]
print(response["title"])

#print(body.decode('utf-8'))

