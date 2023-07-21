from lib.lang import LANG
from lib.driver import DRIVER
from lib.account import ACCOUNT
from lib.facebook import FACEBOOK

from lib.config import CONFIG

import sys

driver = None
account = None
facebook = None
lang = None
config = None
def main():
	global driver, account, facebook, lang, config

	config = CONFIG()

	lang = LANG()

	# driver = DRIVER()
	# account = ACCOUNT(driver)
	# facebook = FACEBOOK(driver)

	user_input()

def user_input():
	status = True
	while status:
		command = str(input("cmd_> ")).lower()

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

		elif command == 'exit':
			print("[i] " + lang.text("program_exit"))
			driver.terminate()
			sys.exit(0)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		driver.terminate()