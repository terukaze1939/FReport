from lib import fb
import sys,time,getpass,random

f = None

def banner():
	banner = """
	FReport

	(MENU)
	- login [Login to facebook account to get cookies]
	- cookie_login [Login using exisiting cookies. This is important command after you've logged in using 'login' command]
	- report_user [Report someone profile using profile id]
	- report_post [Report someone post using post url]
	- rip [Spam #rip hastag on someone timeline]


	(OPTIONAL COMMAND)
	- new_post [Create new post]


	- help [Print this menu]	
	- exit [I'm out]

	"""

	return banner
def main():
	global f
	f = fb.FB()

	usr_input()



def usr_input():
	state = True
	while state:

		cmd = input("_> ")
		cmd = cmd.lower()

		if cmd == "login":
			email = input("email_> ")
			passwd = getpass.getpass("password_> ")

			res = f.login(email, passwd)
			if res[0] == True:
				print("[*] Login successfully")
				f.save_cookies()
			elif res[0] == False and res[1] == "login_checkpoint":
				print("[!] Checkpoint occured")
				code = int(input("approval_code> "))
				check_res = f.checkpoint(code)
				if check_res[0] == True:
					print("[*] Login successfully")
					f.save_cookies()
				elif check_res[0] == False and check_res[1] == "checkpoint_error":
					print("[!!] Checkpoint error, this may facebook need to confirm this device used by useragent to access.")
				else:
					print("[?] Something went wrong, but what? " + check_res[2])
			else:
				print("[?] Something went wrong, but what??? " + res[2])
		elif cmd == "cookie_login":
			f.check()
			print("[*] Current url : " + f.driver.current_url)
		elif cmd == "new_post":
			text = input("text_> ")
			res = f.new_post(text)
			if res[0] == True:
				print("[*] Post has been published ["+res[2]+"]")
			else:
				print("[!] Something went wrong : " +res[2])
		elif cmd == "report_user":
			id = input("profile_id_> ")
			count = int(input("num report_> "))
			for _ in range(count):
				t = random.randint(10,15)

				res = f.report_user(id)
				if res[0] == True:
					print("[*] Report User success")
				else:
					print("[!] Report error")
					break
				print("[i] Sleeping for "+str(t)+" sec")
				time.sleep(t)
		elif cmd == "report_post":
			url = str(input("post_url_> "))
			count = int(input("num report_> "))
			for _ in range(count):
				t = random.randint(10,15)

				res = f.report_post(url)
				if res[0] == True:
					print("[*] Report Post Success")
				else:
					print("[!] " + res[2])
					break
				print("[i] Sleeping for "+str(t)+" sec")
				time.sleep(t)
		elif cmd == "rip":
			id = str(input("profile_id_> "))
			count = int(input("num report_> "))
			for _ in range(count):
				t = random.randint(10,15)

				res = f.rip(id)
				if res[0] == True:
					print("[*] Rip post has been sent : " + res[2])
				else:
					print("[*] Cannot post on someone timeline")
					break
				print("[i] Sleeping for "+str(t)+" sec")
				time.sleep(t)
		elif cmd == "help":
			print(banner())
		elif cmd == "exit":
			state = False
			f.terminate()
			sys.exit(0)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		f.terminate()