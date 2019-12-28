import re
import requests
import configparser

def readConfig(path):
	conf = configparser.ConfigParser()
	conf.read(path, encoding="UTF-8")
	config = {
		'url': conf.get('u2', 'url'),
		'cookies': {
			'c_locale': conf.get('u2', 'c_locale'),
			'nexusphp_u2': conf.get('u2', 'nexusphp_u2')
		},
		'headers': {
			'User-Agent': conf.get('u2', 'User-Agent')
		}
	}
	return config

config = readConfig("config.ini")

class Torrent(object):
	def __init__(self, title, id, promo, detailurl, size):
		self.title = title
		self.id = id
		self.promo = promo
		self.detailurl = detailurl
		self.size = size

	def getDetail(self):
		res = requests.get(url=config['url']+"/"+self.detailurl, cookies=config['cookies'], headers=config['headers'])
		return res.text
	
	def downloadTorrent(self, path):
		res = requests.get(url=config['url']+"/download.php?id="+self.id, cookies=config['cookies'], headers=config['headers'])
		open(path+re.search(r'filename="(.*?)"',res.headers['content-disposition']).group(1),'wb').write(res.content)
		del res

class Promo(object):
	def __init__(self, upload, download):
		self.upload = upload
		self.download = download

class Page(object):
	def __init__(self, index):
		self.index

def searchTorrents(restext):
	#pattern = re.compile(r'<table class="torrentname"(?:.*?)>\n(.*?)</table>')
	pattern = re.compile(r'<tr>\n<td class="rowfollow nowrap" valign="middle">([\d\D]*?</b></a>)</td></tr>')
	rst = pattern.findall(restext)
	return rst

def getTitle(torrent):
	pattern = re.compile(r'<a class="tooltip"(?:.*?)>(.*?)</a>')
	rst = re.search(pattern, torrent).group(1)
	return rst

# detail url, id
def getDetail(torrent):
	pattern = re.compile(r'<a class="tooltip" href="(details.php\?id=(\d*?)&amp;hit=1)"(?:.*?)>')
	rst = re.search(pattern, torrent)
	return rst.group(1), rst.group(2)

def getSize(torrent):
	pattern = re.compile(r'<td class="rowfollow">([\.\d]+)<br />(GiB|MiB)</td>')
	rst = re.search(pattern, torrent)
	return rst.group(1)+' '+rst.group(2)

def getSL(detail):
	pattern = re.compile(r'<div id="peercount"><b>(\d+)个做种者</b> \| <b>(\d+)个下载者</b>')
	rst = re.search(pattern, detail)
	return rst.group(1), rst.group(2)

def getPromo(torrent):
	pattern = re.compile(r'<img class="pro_(.*?)"')
	rst = re.search(pattern, torrent)
	if rst is None:
		return Promo(1, 1)
	pro = rst.group(1)
	if pro == 'free':
		return Promo(1, 0)
	elif pro == 'free2up':
		return Promo(2, 0)
	elif pro == '2up':
		return Promo(2, 1)
	elif pro == '50pctdown':
		return Promo(1, 0.5)
	elif pro == '30pctdown':
		return Promo(1, 0.3)
	elif pro == '50pctdown2up':
		return Promo(2, 0.5)
	elif pro == 'custom':
		pattern = re.compile(r'<img class="arrow(?:up|down)"(?:.*?)><b>(.*?)X')
		rst = pattern.findall(torrent)
		if len(rst) <= 1:
			return Promo(1, 1)
		else:
			return Promo(rst[0], rst[1])
	else:
		return Promo(1, 1)
