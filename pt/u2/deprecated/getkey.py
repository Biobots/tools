import re
import requests
import bs4
import configparser
import classes
import json

conf = configparser.ConfigParser()
conf.read("config.ini", encoding="UTF-8")
apikey = conf.get('u2', 'apikey')

url = "https://u2.dmhy.org/jsonrpc_torrentkey.php?apikey="+apikey
data = [
	{
		"jsonrpc": "2.0", 
		"method": "query", 
		"params": [ "ffb6c7b21d38a9ec9f097f96f2c89e4b20068897" ], 
		"id": 1
	}, 
  	{
		"jsonrpc": "2.0", 
		"method": "query", 
		"params": [ "f8c75a145eef644eb201a28088d8d652be95e57b" ], 
		"id": 2
  	}
]
data = json.dumps(data)
headers = {'Content-Type':'application/json'}
res = requests.post(url, data=data, headers=headers)
print(res.text)