import json

from lib.config import CONFIG

class LANG:
	def __init__(self):
		self.lang = None
		self.config = CONFIG().get()
		with open("./lang/"+self.config["lang"]+".json") as file:
			self.lang = json.loads(file.read())

	def text(self, key):
		return self.lang[key]
