from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pickle,time,json

class FB:
	def __init__(self):
		self.ua = """Mozilla/5.0 (Linux; Android 11; MP02 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36[FBAN/EMA;FBLC/es_ES;FBAV/289.0.0.18.116;]"""


		self.service = Service(ChromeDriverManager().install())
		self.options = Options()
		self.options.add_argument('user-agent='+self.ua)
		self.options.add_argument('--disable-extension')
		self.options.add_argument('--headless')
		self.options.add_argument('--no-sandbox')
		self.options.add_argument('--disable-gpu')
		self.options.add_argument('--log-level=1')
		self.driver = webdriver.Chrome(service=self.service, options=self.options)

		self.url_profile = "https://m.facebook.com/profile.php"
		self.url_login = "https://m.facebook.com/login.php"
		self.url_home = "https://m.facebook.com/home.php"
		self.profile_target = "https://m.facebook.com/profile.php?id={}"

	def input(self, name, value):
		self.driver.find_element(By.XPATH, "//input[@name='"+name+"']").send_keys(value)
	def submit(self, name):
		self.driver.find_element(By.XPATH, "//input[@type='"+name+"']").click()
	def get_element(self,element, name, val):
		return self.driver.find_element(By.XPATH, "//"+element+"[@"+name+"='"+val+"']")
	def get_elements(self, element, name, val):
		return self.driver.find_elements(By.XPATH, "//"+element+"[@"+name+"='"+val+"']")

	def load(self,url):
		self.driver.get(url)


	def check(self):
		self.load(self.url_login)
		self.load_cookies()
		self.load(self.url_home)

		if '¿Qué estás pensando?' in self.driver.page_source:
			return (True, "check_success", "check()")
		else:
			return (False, "check_error", "check()")

	def checkpoint(self, value):
		self.input("approvals_code", value)
		self.submit("submit")

		if 'Recordar navegador' in self.driver.page_source:
			self.submit('submit')
			if 'home' in self.driver.current_url:
				return (True, "login_success", "checkpoint()")
			elif 'Ver un intento de inicio de sesión reciente' in self.driver.page_source:
				return (False, "checkpoint_error", "checkpoint(session)")
			else:
				return (False, None, "checkpoint(home)")
		else:
			return (False,None, "checkpoint(save browser)")

	def login(self, email, passwd):
		self.load(self.url_login)

		if 'login' in self.driver.current_url:
			print("[*] Login page")
			self.input('email', email)
			self.input('pass', passwd)
			self.submit('submit')

			if 'checkpoint' in self.driver.current_url:
				return (False, "login_checkpoint", "login()")
			elif 'home' in self.driver.current_url:
				return (True, "login_success", "login()")
			elif 'La contraseña que has introducido es incorrecta.' in self.driver.page_source:
				return (False, "login_error", "invalid password")
			elif 'Has usado una contraseña antigua' in self.driver.page_source:
				return (False, "login_error", "you're entered old password")
			elif 'save-device' in self.driver.current_url:
				self.submit('submit')
				if '¿Qué estás pensando?' in self.driver.page_source:
					return (True, "login_success", "login()")
				elif 'gettingstarted' in self.driver.current_url:
					self.get_element('a', 'class', 'ba z').click()
					if 'home' in self.driver.current_url:
						return (True, "login_success", "login()")
					else:
						return (False, "login_error", ":((")
				else:
					return (False, "login_error", ":(")
			else:
				return (False, "login_error", "login()")

		else:
			return (False, None, "login(s)")

	def new_post(self, text):
		self.load(self.url_profile)
		self.get_element("textarea","name","xc_message").send_keys(text)
		self.get_element("input", "name", "view_post").click()


		href = self.driver.find_element(By.XPATH, "//div[@role='article']/div[2]/div[2]/a[1]").get_attribute('href')
		if href != "" or href != None:
			return (True, "new_post_success", str(href))
		else:
			return (False, "new_post_error", "no_data")

	def report_user(self, id):
		print("[*] Opening profile url")
		self.load(self.profile_target.replace("{}", id))
		print("[*] Opening profile options")
		print("[i] User : " +self.driver.title)
		self.driver.find_element(By.XPATH,"//a[text()='Más']").click()
		print("[*] Clicking on 'find help or report profile'")
		self.driver.find_element(By.XPATH,"//a[text()='Buscar ayuda o denunciar perfil']").click()
		print("[*] Choosing 'fake account'")
		self.driver.find_element(By.XPATH, "//span[text()='Cuenta falsa']").click()
		print("[*] Submitting ")
		self.driver.find_element(By.XPATH, "//input[@name='action' and @type='submit']").click()
		print("[*] Confirm report")
		self.driver.find_element(By.XPATH, "//input[@type='checkbox' and @name='checked']").click()
		self.driver.find_element(By.XPATH, "//input[@name='action' and @type='submit']").click()
		if 'Confirmación de la denuncia' in self.driver.page_source:
			return (False, "report_user_failed", "report_user()")
		else:
			return (True, "report_user_success", "report_user()")


	def report_post(self, url):
		print("[*] Opening post")
		self.load(url)
		if 'Más' in self.driver.page_source:
			print("[*] Opening post options")
			self.driver.find_element(By.XPATH, "//a[text()='Más']").click()
			print("[*] Choosing 'Report post'")
			self.driver.find_element(By.XPATH, "//input[@value='RESOLVE_PROBLEM']").click()
			print("[*] Submitting")
			self.driver.find_element(By.XPATH, "//input[@type='submit' and @name='submit']").click()
			print("[*] Choosing 'spam'")
			self.driver.find_element(By.XPATH, "//input[@type='radio' and @value='spam']").click()
			print("[*] Submitting")
			self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

			if 'Selecciona un problema' in self.driver.page_source:
				return (False, 'report_post_failed', 'report_post()')
			else:
				return (True, 'report_post_success','report_post()')
		else:
			return (False, "user_not_found", "report_post()")




	def save_cookies(self):
		cookie = self.driver.get_cookies()
		
		with open('./cookies/mycookie.pkl', 'wb') as file:
			pickle.dump(cookie, file)
			print("[*] Cookies saved to cookies/mycookie.txt")

	def load_cookies(self):
		with open('./cookies/mycookie.pkl', 'rb') as file:
			cookies = pickle.load(file)

			for cookie in cookies:
				self.driver.add_cookie(cookie)
			print("[*] Cookies loaded")

	def terminate(self):
		self.driver.close()
		# pass
