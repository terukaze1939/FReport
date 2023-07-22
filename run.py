from lib.lang import LANG
from lib.driver import DRIVER
from lib.account import ACCOUNT
from lib.facebook import FACEBOOK

from lib.config import CONFIG

import sys, os, getpass, random
from time import sleep

driver = None
account = None
facebook = None
lang = None
config = None

def help_banner():
	print("""---Help---
	# Account
	login\t\t\t: """+lang.text("banner_login_desc")+"""
	cookie_login\t\t: """+lang.text("banner_cookie_login_desc")+"""

	# Facebook
	rip_spam\t\t: """+lang.text("banner_rip_spam_desc")+"""
	report_user\t\t: """+lang.text("banner_report_user_desc")+"""
	report_post\t\t: """+lang.text("banner_report_post_desc")+"""

	# Configuration
	set_default_login\t: """+lang.text("banner_set_default_login_desc")+"""
	set_checkpoint\t\t: """+lang.text("banner_set_checkpoint_desc")+"""
	set_lang\t\t: """+lang.text("banner_set_lang_desc")+"""

	# Other
	restart_driver\t\t: """+lang.text("banner_restart_driver_desc")+"""
	config\t\t\t: """+lang.text("banner_config_desc")+"""
	clear\t\t\t: """+lang.text("banner_clear_desc")+"""
	exit\t\t\t: """+lang.text("banner_exit_desc"))

def main():
	global driver, account, facebook, lang, config

	config = CONFIG()

	lang = LANG()

	driver = DRIVER().get()
	if driver == False:
		print("[!] "+lang.text("unsupported_device"))
		sys.exit(0)

	account = ACCOUNT(driver)
	facebook = FACEBOOK(driver)

	user_input()

def clear_terminal():
	if sys.platform == 'win32':
		os.system('cls')
	elif sys.platform == 'linux':
		os.system('clear')
	

def user_input():
	global driver, account, facebook
	status = True
	while status:
		config.reload_config()
		command = str(input("cmd_> "))

		# user

		if command == "new_post":
			text = str(input("text_> "))
			if text == "":
				print("[!] " +lang.text("profile_create_new_post_text_blank"))
			else:
				result = facebook.new_post(text)
				if result != False:
					print("[+] "+lang.text("profile_create_new_post_ok") + " : " +result[1])
				else:
					print("[!] "+lang.text("profile_create_new_post_error"))



		# end user

		# config
		if 'set_default_login' in command:
			command_args = command.split(" ")
			if len(command_args) > 1:
				if command_args[1] == "manual":
					print("[i] "+lang.text("set_default_login_to_manual"))
					config.set_default_login("manual")
				elif command_args[1] == "cookie_login":
					print("[i] "+lang.text("set_default_login_to_cookie_login"))
					config.set_default_login("cookie_login")
				else:
					print("[i] " + lang.text("set_default_login_arg_not_found").replace("?", command_args[1]))
			else:
				print("[i] " + lang.text("set_default_login_not_found"))

		elif 'set_lang' in command:
			command_args = command.split(" ")
			if len(command_args) > 1:
				if command_args[1] in lang.available_lang:
					print("[i] " + lang.text("set_lang").replace("?", command_args[1]))
					config.set_lang(command_args[1])
				else:
					print("[i] "+lang.text("set_lang_not_found").replace("?", command_args[1]).replace("@", str(lang.available_lang)))
			else:
				print("[!] "+lang.text("set_lang_arg_error"))


		elif 'set_checkpoint' in command:
			command_args = command.split(" ")
			if len(command_args) > 1:
				if command_args[1] == "skip":
					print("[i] " + lang.text("set_checkpoint_to_skip"))
					config.set_checkpoint("skip")
				elif command_args[1] == "noskip":
					print("[i] "+ lang.text("set_checkpoint_to_noskip"))
					config.set_checkpoint("noskip")
				else:
					print("[i] "+lang.text("set_checkpoint_arg_not_found"))
			else:
				print("[!] " + lang.text("set_checkpoint_arg_error"))

		# end config

		# account

		if command == 'login':
			driver.delete_all_cookies()
			if config.get()["default_login"] == "cookie_login":
				print("[i] "+lang.text("login_cookie_msg"))
				last_logged_in_email = config.get()["last_logged_in_email"]

				result = account.cookie_login(last_logged_in_email)
				if result[0] == True:
					print("[+] "+lang.text("login_cookie_ok"))
				else:
					print("[+] "+lang.text("login_cookie_error"))
			else:

				email = str(input('email_> '))
				passwd = str(getpass.getpass('password_> '))

				if email != '':
					if passwd != '':
						res = account.login(email, passwd)
						if res[0] == True:
							if res[1] == "login_save_device":
								result = account.save_device()
								if result[0] == True:
									print("[+] "+lang.text("login_ok"))
								else:
									print("[!] "+lang.text("login_save_device_err"))
							elif res[1] == "login_ok":
								print("[+] " + lang.text("login_ok"))
							config.set_last_logged_in_email(email)
							account.save_cookies(email)
						elif res[0] == False:
							if res[1] == "login_checkpoint":
								if config.get()["checkpoint"] == "noskip":
									code = str(input("approval code_> "))
									result = account.checkpoint(code)
									if result[0] == True:
										print("[+] "+lang.text("login_checkpoint_ok"))
										print("[+] "+lang.text("login_ok"))
										config.set_last_logged_in_email(email)
										account.save_cookies(email)
									elif result[0] == False:
										if result[1] == "login_checkpoint_verify_err":
											print("[!] "+lang.text("login_checkpoint_verify_err"))
										elif result[1] == "login_checkpoint_err":
											print("[!] "+lang.text("login_checkpoint_err"))
										elif result[1] == "login_checkpoint_code_err":
											print("[!] "+lang.text("login_checkpoint_code_err_msg"))
								else:
									print("[i] "+lang.text("config_checkpoint_msg"))
							elif res[1] == "login_form_invalid":
								print("[!] "+lang.text("login_form_invalid"))
							elif res[1] == "login_invalid_old_password":
								print("[!] " + lang.text("login_invalid_old_password"))
							else:
								print("[!] " + lang.text("login_err"))

					else:
						print("[!] "+ lang.text("login_password_blank"))
				else:
					print("[!] " + lang.text("login_email_blank"))

		# end account


		# facebook

		elif command == 'rip_spam':
			profile_id = str(input("profile_id_> "))
			num = int(input("num_> "))

			if profile_id =="":
				print("[!] "+lang.text("input_profile_id"))
			elif num <= 0:
				print("[!] "+lang.text("input_num_loop"))
			else:
				info("RIP Spammer", profile_id, num)
				for i in range(num):
					randint = random.randint(8,40)
					result = facebook.rip(profile_id)

					if result[0] == True:
						print("[+] "+lang.text("rip_success") + " : "+result[1])
					else:
						print("[!] "+lang.text(result[1]))
						break
					if i+1 < num:
						print("[*] "+lang.text("sleeping").format(str(randint)))
						sleep(randint)
		elif command == "report_user":
			profile_id = str(input("profile_id_> "))
			num = int(input("num_> "))

			if profile_id == "":
				print("[!] "+lang.text("input_profile_id"))
			elif num <= 0:
				print("[!] "+lang.text("input_num_loop"))
			else:
				info("REPORT_USER", profile_id, num)
				for i in range(num):
					randint = random.randint(8,18)

					result = facebook.report_user(profile_id)
					if result[0] == True:
						print("[+] "+lang.text(result[1]))
					else:
						if result[1] == 'report_user_not_found':
							print("[!] "+lang.text(result[1]))
							break
						elif result[1] == 'report_user_error':
							print("[!] "+lang.text(result[1]))
							break

					if i+1 < num:
						print("[*] "+lang.text("sleeping").format(str(randint)))
						sleep(randint)

		elif command == "report_post":
			post_url = str(input("url_> "))
			num = int(input("num_> "))

			if post_url == "":
				print("[!] "+lang.text("input_post_url"))
			elif num <= 0:
				print("[!] "+lang.text("input_num_loop"))
			else:
				info("REPORT_POST", post_url, num)
				for i in range(num):
					randint = random.randint(8,10)

					result = facebook.report_post(post_url)
					if result[0] == True:
						print("[+] "+lang.text(result[1]))
					else:
						print("[!] "+lang.text(result[1]))
						break
					if i+1 < num:
						print("[*] "+lang.text("sleeping").format(str(randint)))
						sleep(randint)


		# end facebook

		elif command == 'restart_driver':
			print("[*] " +lang.text("restart_driver"))
			driver.close()
			driver = DRIVER().get()
			account = ACCOUNT(driver)
			facebook = FACEBOOK(driver)

		elif command == 'help':
			help_banner()

		elif command == 'config':
			print(config.get())
			print(driver.execute_script("return navigator.userAgent"))

		elif command == 'clear':
			clear_terminal()

		elif command == 'exit':
			print("[i] " + lang.text("program_exit"))
			driver.close()
			sys.exit(0)


def info(feature, target, num):
	text = """
	Using ["""+feature+"""] Feature
	Target\t\t: """+str(target)+"""
	Num of loops\t: """+str(num)+"""

	"""
	print(text)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		driver.close()