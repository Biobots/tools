from utils import *

#ret = requests.get(url=config['url']+"/torrents.php", cookies=config['cookies'], headers=config['headers'])
#rst = searchTorrents(ret.text)
torrent = []
num = int(input("How many torrents to show:"))
trturl = config['url']+"/torrents.php?page="
count = 0
pagecount = 0
while (count <= num):
	if count >= num: break
	ret = requests.get(url=trturl+str(pagecount), cookies=config['cookies'], headers=config['headers'])
	rst = searchTorrents(ret.text)
	for i in rst:
		if count >= num: break
		url, id = getDetail(i)
		torrent.append(Torrent(getTitle(i), id, getPromo(i), url, getSize(i)))
		count += 1
	pagecount += 1
for i in torrent:
	print(i.title)
	print(i.detailurl)
	print(i.size)