from lib.driver import DRIVER
from selenium.webdriver.common.by import By
from lib.url import URL
from lib.lang import LANG
import uuid


class FACEBOOK:
	def __init__(self, driver):
		self.driver = driver
		self._url = URL()
		self.lang = LANG()
		self.rip_text = """#RIP I am so sorry to hear about your loss. May you find comfort in the love and support of those around you {}"""


	def rip(self, profile_id):
		self.driver.get(self._url.profile_target.replace("{}", profile_id))

		if 'pikirkan?' in self.driver.page_source:
			randid = uuid.uuid4()

			self.driver.find_element(By.XPATH, "//textarea[@name='xc_message']").send_keys(self.rip_text.replace("{}", str(randid)))
			self.driver.find_element(By.XPATH, "//input[@name='view_post']").click()

			# href = self.driver.find_element(By.XPATH, "//div[@role='article']/div[2]/div[3]/a[2]").get_attribute("href")
			href = self.driver.find_elements(By.XPATH, "//a[text()='Berita Lengkap']")[0].get_attribute('href')

			return (True, href)
		else:
			return (False, "rip_err")

	def report_user(self, profile_id):
		self.driver.get(self._url.profile_target.format(str(profile_id)))

		if 'Lainnya' in self.driver.page_source:


			self.driver.find_element(By.XPATH, "//a[text()='Lainnya']").click()
			self.driver.find_element(By.XPATH, "//a[text()='Cari dukungan atau laporkan profil']").click()
			self.driver.find_element(By.XPATH, "//span[text()='Akun Palsu']").click()
			self.driver.find_element(By.XPATH, "//input[@name='action' and @type='submit']").click()
			self.driver.find_element(By.XPATH, "//input[@type='checkbox' and @name='checked']").click()
			self.driver.find_element(By.XPATH, "//input[@name='action' and @type='submit']").click()

			if 'Konfirmasi laporan' in self.driver.page_source:
				return (False, 'report_user_error')
			else:
				return (True, 'report_user_ok')
		else:
			return (False, 'report_user_not_found')

	def report_post(self, url_post):
		self.driver.get(url_post)

		if 'Lainnya' in self.driver.page_source:
			self.driver.find_element(By.XPATH, "//a[text()='Lainnya']").click()
			self.driver.find_element(By.XPATH, "//input[@value='RESOLVE_PROBLEM']").click()
			self.driver.find_element(By.XPATH, "//input[@type='submit' and @name='submit']").click()
			self.driver.find_element(By.XPATH, "//input[@type='radio' and @value='spam']").click()

			self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

			self.driver.find_element(By.XPATH, "//input[@type='checkbox' @name='checked']").click()
			self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

			if 'Konfirmasi laporan' in self.driver.page_source:
				return (False, 'report_post_error')
			else:
				return (True, 'report_post_ok')
		else:
			return (False, 'report_post_not_found')



	def new_post(self, text):
		self.driver.get(self._url.profile_user)
		self.driver.find_element(By.XPATH, "//textarea[@name='xc_message']").send_keys(text)
		self.driver.find_element(By.XPATH, "//input[@type='submit' and @name='view_post']").click()

		href = self.driver.find_elements(By.XPATH, "//a[text()='Berita Lengkap']")[0].get_attribute('href')
		if href =="":
			return False
		else:
			return (True, href)
