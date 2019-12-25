import re
import requests
import bs4
import configparser
import classes

def calpromo(taglist):
	if len(taglist) == 0:
		return classes.Promo(1, 1)
	else:
		tag = taglist[0]
		text = tag['class'][0]
		if text == 'pro_free':
			return classes.Promo(1, 0)
		elif text == 'pro_free2up':
			return classes.Promo(2, 0)
		elif text == 'pro_2up':
			return classes.Promo(2, 1)
		elif text == 'pro_50pctdown':
			return classes.Promo(1, 0.5)
		elif text == 'pro_30pctdown':
			return classes.Promo(1, 0.3)
		elif text == 'pro_50pctdown2up':
			return classes.Promo(2, 0.5)
		elif text == 'pro_custom':
			if len(taglist) >= 3:
				up = re.sub(r'X', "", taglist[1].next_sibling.text)
				down = re.sub(r'X', "", taglist[2].next_sibling.text)
				return classes.Promo(up, down)
			else:
				return classes.Promo(1, 1)
		else:
			return classes.Promo(1, 1)

class Torrent(object):
	def __init__(self, title, id, promo):
		self.title = title
		self.id = id
		self.promo = promo

class Promo(object):
	def __init__(self, upload, download):
		self.upload = upload
		self.download = download

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

def searchTorrents(restext):
	pattern = re.compile(r'<table class="torrentname"(?:.*?)>\n(.*?)</table>')
	rst = pattern.findall(restext)
	return rst

def getName(torrent):
	pattern = re.compile(r'<a class="tooltip"(?:.*?)>(.*?)</a>')
	rst = re.search(pattern, torrent).group(1)
	return rst

# detail url, id
def getDetail(torrent):
	pattern = re.compile(r'<a class="tooltip" href="(details.php\?id=(\d*?)&amp;hit=1)"(?:.*?)>')
	rst = re.search(pattern, torrent)
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
		return classes.Promo(2, 0.5)
	elif pro == 'custom':
		pattern = re.compile(r'<img class="arrow(?:up|down)"(?:.*?)><b>(.*?)X')
		rst = pattern.findall(torrent)
		if len(rst) <= 1:
			return Promo(1, 1)
		else:
			return Promo(rst[0], rst[1])
	else:
		return Promo(1, 1)