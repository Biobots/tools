class Torrent(object):
	def __init__(self, title, id, promo):
		self.title = title
		self.id = id
		self.promo = promo

class Promo(object):
	def __init__(self, upload, download):
		self.upload = upload
		self.download = download