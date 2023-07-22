import json

class CONFIG:
	def __init__(self):
		with open('./config.json', 'r') as file:
			self.conf = json.loads(file.read())

	def get(self):
		self.reload_config()
		return self.conf

	def reload_config(self):
		with open('./config.json', 'r') as file:
			self.conf = json.loads(file.read())

	def set_default_login(self, login):
		self.reload_config()
		temp_data = {}
		for k,v in self.conf.items():
			if k == "default_login":
				temp_data[k] = login
			else:
				temp_data[k] = v

		encoded = json.dumps(temp_data, sort_keys=True, indent=4)
		self.write(encoded)

	def set_lang(self, lang):
		self.reload_config()
		temp_data = {}
		for k, v in self.conf.items():
			if k == "lang":
				temp_data[k] = lang
			else:
				temp_data[k] = v

		encoded = json.dumps(temp_data, sort_keys=True, indent=4)
		self.write(encoded)

	def set_checkpoint(self, do):
		self.reload_config()
		temp_data = {}
		for k,v in self.conf.items():
			if k == "checkpoint":
				temp_data[k] = do
			else:
				temp_data[k] = v

		encoded = json.dumps(temp_data, sort_keys=True, indent=4)
		self.write(encoded)

	def set_last_logged_in_email(self,email):
		self.reload_config()
		temp_data = {}
		for k,v in self.conf.items():
			if k == "last_logged_in_email":
				temp_data[k] = email
			else:
				temp_data[k] = v

		encoded = json.dumps(temp_data, sort_keys=True, indent=4)
		self.write(encoded)

	def write(self, data):
		with open('./config.json', 'w') as file:
			file.write(data)
			file.close()