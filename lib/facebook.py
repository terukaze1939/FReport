from lib.driver import DRIVER
from selenium.webdriver.common.by import By
from lib.url import URL
import uuid


class FACEBOOK:
	def __init__(self, driver):
		self.driver = driver
		self._url = URL()
		self.rip_text = """#RIP I am so sorry to hear about your loss. May you find comfort in the love and support of those around you {}"""


	def RIP(self, profile_id):
		self.driver.get(self._url.profile_target.replace("{}", profile_id))

		if '#apa-yang-kamu-pikirkan' in self.driver.page_source:
			randid = uuid.uuid4()

			self.driver.find_element(By.XPATH, "//textarea[@name='xc_message']").send_keys(self.rip_text.replace("{}", str(randid)))
			self.driver.find_element(By.XPATH, "//input[@name='view_post']").click()

			href = self.driver.find_element(By.XPATH, "//div[@role='article']/div[2]/div[3]/a[2]").get_attribute("href")

			return (True, href)
		else:
			return (False, "rip_err")