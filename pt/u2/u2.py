import re
import requests
import bs4
import configparser
import classes
from utils import *

ret = requests.get(url=config['url']+"/torrents.php", cookies=config['cookies'])
rst = searchTorrents(ret.text)
torrent = []
for i in rst:
	url, id = getDetail(i)
	print(config['url']+'/'+url+'\n'+id)
	promo = getPromo(i)
	print(str(promo.upload)+" "+str(promo.download))
	torrent.append(Torrent(getTitle(i), id, promo, url))
f = torrent[0].getTorrent()
open("./"+torrent[0].id+".torrent",'wb').write(f.content)
del f