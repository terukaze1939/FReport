from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from lib.config import CONFIG
import sys

class DRIVER:
	def __init__(self):
		self.config = CONFIG().get()
		self.ua = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 [FBAN/EMA;FBLC/id_ID;FBAV/289.0.0.18.116;]"""
		

		self.opt = Options()
		self.opt.add_argument('--lang=id_ID')
		self.opt.add_argument('--locale=id_ID')
		self.opt.add_argument('--no-sandbox')
		self.opt.add_argument('--disable-gpu')
		self.opt.add_argument('--log-level=1')
		self.opt.add_argument('--disable-dev-shm-usage')
		self.opt.add_argument('user-agent='+self.ua)


	def get(self):
		return self.platform()

	def platform(self):
		if sys.platform == 'win32' or sys.platform == 'win64':
			self.opt.add_experimental_option('excludeSwitches', ['enable-automation'])
			self.opt.add_experimental_option('useAutomationExtension', False)
			self.opt.add_argument('--headless')

			service = Service(ChromeDriverManager().install())
			return webdriver.Chrome(service=service, options=self.opt)

		elif sys.platform == 'linux':
			self.opt.add_argument('--headless=new')
			return webdriver.Chrome(options=self.opt)

		else:
			return False

	def terminate(self):
		self.driver.close()