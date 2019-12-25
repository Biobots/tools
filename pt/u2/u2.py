import re
import requests
import bs4
import configparser
import classes
import utils

config = utils.readConfig("config.ini")
ret = requests.get(url=config['url']+"/torrents.php", cookies=config['cookies'])
rst = utils.searchTorrents(ret.text)
for i in rst:
	url, id = utils.getDetail(i)
	print(config['url']+'/'+url+'\n'+id)
	promo = utils.getPromo(i)
	print(str(promo.upload)+" "+str(promo.download))