from utils import *

ret = requests.get(url=config['url']+"/torrents.php", cookies=config['cookies'], headers=config['headers'])
rst = searchTorrents(ret.text)
torrent = []
for i in rst:
	url, id = getDetail(i)
	#print(config['url']+'/'+url+'\n'+id)
	promo = getPromo(i)
	#print(str(promo.upload)+" "+str(promo.download))
	torrent.append(Torrent(getTitle(i), id, promo, url))
torrent[1].downloadTorrent("./")