import changes
import socket
import datetime
import sys

class IrcBot():

	def __init__(self):

		# Setting up variables
		if len(sys.argv) < 3:
			self.server = "chmielecki.pro"
			self.channel = "#zmiany"
		else:
			self.server = argv[1]
			self.channel = argv[2]

		try:
			self.botnick = argv[3]
		except:
			self.botnick = "vlo_bot"

		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Automatic changes
		self.at_nine = True
		self.at_six = True

		print("[+] Connecting to {}".format(self.server))
		self.conn.connect((self.server, 6667)) # connect to server

		# Authenticate
		self.conn.send("NICK {}\n".format(self.botnick).encode())
		self.conn.send("USER {} 8 * :{}\n".format(self.botnick, "Dobry bot do wrzucania zmian ;;;;))))").encode())
		self.conn.send("JOIN {}\n".format(self.channel).encode())

		print("[+] Connected to {}".format(self.server))


	def privmsg(self, message, nick=None):
		if nick:
			self.conn.send("PRIVMSG {}:{} :{}\r\n".format(self.channel, nick, message).encode())
		else:
			self.conn.send("PRIVMSG {} :{}\r\n".format(self.channel, message).encode())

	def stay_alive(self, text):
		print("[!] Received PING. Sending response to server.")
		self.conn.send("PONG {}\r\n".format(text.split()[1]).encode())
		print("[!] Sent PONG.")


	def main_loop(self):
		while 1:
			text = self.conn.recv(2048).decode()
			# Optional logging in case someting breaks
			# print("[*] Received: {}".format(text))

			# Staying alive
			if "PING" == text[0:4]:
				self.stay_alive(text)

			# Various commands
			# More to come ofc
			elif "!changes" in text:
				self.cmd_changes()

			elif "!idea" in text:
					self.cmd_getidea(text)

			self.auto_changes_at_given_times()


	def auto_changes_at_given_times(self):
		if datetime.datetime.now().hour == 21 and not self.at_nine:
			self.at_nine = True
			self.privmsg(".: Automatic update at 21:00 :.")
			self.cmd_changes()
		elif datetime.datetime.now().hour == 6 and not self.at_six:
			self.at_six = True
			self.privmsg(".: Automatic update at 6:00 :.")
			self.cmd_changes()
		elif datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 1:
			# Reset state at midnight
			self.at_six = False
			self.at_nine = False


	def cmd_changes(self):
		self.privmsg("Fetching...")
		chg = changes.Changes().irc_changes()
		self.privmsg("Here you go:")
		if chg:
			for line in chg:
				self.privmsg(line[0])
				for x in line[1:]:
					self.privsmg("    " + x)
		else:
			self.privmsg(".! No changes !.")


	def cmd_getidea(self, text):
		# Extract idea
		try:
			idea = text.split(":")[2]
			idea = idea[6:]
			print("[!] IDEA - {}".format(idea.strip()))
			self.privmsg("Idea \"{}\" registered!".format(idea.strip()))
		except:
			self.privmsg(".! No idea given !.")
		# Open file and write idea
		# Optionally database

bot = IrcBot()
bot.main_loop()
