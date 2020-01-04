from utils import *
import os

command = 0

def printOption(trtlist, selected):
	index = 0
	for i in torrent:
		color = ''
		if index == selected:
			color = '\033[1;32m'
		print(color+str(index)+': '+i.title)
		print('  体积: '+i.size+'  优惠: UP:'+str(i.promo.upload)+' | DOWN: '+str(i.promo.download))
		if index == selected:
			s, l = getSL(i.getDetail())
			print('  上传: '+str(s)+' | 下载: '+str(l)+'\033[0m')
		index += 1
	index -= 1
	return

def move(offset, num):
	global command
	command += offset
	if (command >= num): command = num - 1
	if (command <= 0): command = 0

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
while True:
	os.system('clear')
	printOption(torrent, command)
	c = input("choose one or press enter:")
	if c == '':
		name = torrent[command].downloadTorrent('./')
		#os.system('transmission-remote -a '+name)
		break
	else:
		command = int(c)