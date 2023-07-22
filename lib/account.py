from lib.url import URL
from lib.lang import LANG
from selenium.webdriver.common.by import By
import pickle

class ACCOUNT:
	def __init__(self, driver):
		self.driver = driver
		self._url = URL()
		self.lang = LANG()

	def login(self, email, passwd):
		# open login page
		self.driver.get(self._url.login)
		
		# fill login form and submit
		self.driver.find_element(By.XPATH, "//input[@name='email']").send_keys(email)
		self.driver.find_element(By.XPATH, "//input[@name='pass']").send_keys(passwd)
		self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

		if 'checkpoint' in self.driver.current_url:
			return (False, "login_checkpoint")
		elif 'home' in self.driver.current_url:
			return (True, "login_ok")
		elif self.lang.text("login_form_invalid") in self.driver.page_source:
			return (False, "login_form_invalid")
		elif self.lang.text("login_invalid_old_password") in self.driver.page_source:
			return (False, "login_invalid_old_password")
		elif 'save-device' in self.driver.current_url:
			return (True, "login_save_device")
		else:
			return (False, "login_err")

	def cookie_login(self, email):
		self.driver.get(self._url.login)
		self.load_cookies(email)
		self.driver.get(self._url.home)

		if 'Apa yang Anda pikirkan sekarang' in self.driver.page_source:
			return (True, "login_cookie_ok")
		else:
			return (False, "login_cookie_error")

	def save_device(self):
		self.driver.find_element(By.XPATH,"//input[@type='submit']").click()
		if 'Apa yang Anda pikirkan sekarang' in self.driver.page_source:
			return (True, "login_ok")
		elif 'gettingstarted' in self.driver.current_url:
			self.driver.find_element(By.XPATH, "//a[@class='ba z']").click()
			if 'home' in self.driver.current_url:
				return (True, "login_ok")
			else:
				return (False, "login_err")
		else:
			return (False, "login_err")

	def checkpoint(self, code):
		self.driver.find_element(By.XPATH, "//input[@name='approvals_code']").send_keys(code)
		self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

		if "Ingat Browser" in self.driver.page_source or "Simpan Browser" in self.driver.page_source:
			self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
			if 'home' in self.driver.current_url:
				return (True, "login_checkpoint_ok")
			elif "Tinjau Upaya" in self.driver.page_source:
				return (False, "login_checkpoint_verify_err")
			else:
				return (False, "login_checkpoint_err")

		elif "Tinjau Upaya" in self.driver.page_source:
			return (False, "login_checkpoint_verify_err")

		elif "tidak cocok" in self.driver.page_source:
			return (False, "login_checkpoint_code_err")
		else:
			return (False, "login_checkpoint_err")


	def save_cookies(self, username):
		cookies = self.driver.get_cookies()
		with open("./cookies/"+username+"_cookies.pkl", "wb") as file:
			pickle.dump(cookies, file)
			# cookies saved

	def load_cookies(self, username):
		with open("./cookies/"+username+"_cookies.pkl", "rb") as file:
			cookies = pickle.load(file)
			for cookie in cookies:
				self.driver.add_cookie(cookie)
			# cookies loaded
