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

conf = configparser.ConfigParser()
conf.read("config.ini", encoding="UTF-8")
url = conf.get('u2', 'url') + "/torrents.php"
headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
}
cookies = {
	'c_locale': conf.get('u2', 'c_locale'),
	'nexusphp_u2': conf.get('u2', 'nexusphp_u2')
}
ret = requests.get(url=url, cookies=cookies)
soup = bs4.BeautifulSoup(ret.text, "lxml")
rst = soup.select('.torrentname')
for r in rst:
	name = r.select('.tooltip')
	title = name[0].text
	url = name[0]['href']
	id = re.sub(r'(details.php\?id=)|(&hit=1)', "", url)
	tr = r.select('tr')[-1]
	taglist = tr.select('img')
	promo = calpromo(taglist)
	torrent = classes.Torrent(title, id, promo)
	print(torrent.id + " UP:" + str(torrent.promo.upload) + " DOWN:" + str(torrent.promo.download) + " " + torrent.title + "\nurl:" + conf.get('u2', 'url') + "/details.php?id=" + id)