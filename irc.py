import socket
import changes
import datetime


class IrcBot():

	def __init__(self):
		# Setting up variables
		self.server = "chmielecki.pro"
		self.channel = "#zmiany"
		self.botnick = "vlo_bot"
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Automatic changes
		self.at_nine = True
		self.at_six = True

		print("[+] Connecting to {}".format(self.server))
		self.irc.connect((self.server, 6667)) # connect to server

		# Authenticate
		self.irc.send("NICK {}\n".format(self.botnick).encode())
		self.irc.send("USER {} 8 * :{}\n".format(self.botnick, "Dobry bot do wrzucania zmian ;;;;").encode())
		self.irc.send("JOIN {}\n".format(self.channel).encode())

		print("[+] Connected to {}".format(self.server))


	def main_loop(self):
		while 1:
			text = self.irc.recv(2048).decode()
			# Optional logging ig someting breaks
			# print("[*] Received: {}".format(text))

			# Staying alive
			if "PING" in text:
				print("\n\t[!] Received PING. Sending response to server.\n")
				self.irc.send("PONG {}\r\n".format(text.split()[1]).encode())
				print("\n\t[!] Sent PONG.\n")

			# Various commands
			# More to come ofc

			elif "!changes" in text:
				self.cmd_changes()

			self.auto_changes_at_given_times()


	def auto_changes_at_given_times(self):
		if datetime.datetime.now().hour == 21 and not self.at_nine:
			self.at_nine = True
			self.irc.send("PRIVMSG {} :.: Automatic update at 21:00 :.\r\n".format(self.channel).encode())
			self.cmd_changes()

		elif datetime.datetime.now().hour == 6 and not self.at_six:
			self.at_six = True
			self.irc.send("PRIVMSG {} :.: Automatic update at 6:00 :.\r\n".format(self.channel).encode())
			self.cmd_changes()

		elif datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 1:
			# Reset state at midnight
			self.at_six = False
			self.at_nine = False

	def cmd_changes(self):
		self.irc.send("PRIVMSG {} :Fetching...\r\n".format(self.channel).encode())
		chg = changes.Changes().irc_changes()
		self.irc.send("PRIVMSG {} :Here you go:\r\n".format(self.channel).encode())
		if chg:
			for line in chg:
				self.irc.send("PRIVMSG {} :{}\r\n".format(self.channel, line[0]).encode())
				for x in line[1:]:
					self.irc.send("PRIVMSG {} :    {}\r\n".format(self.channel, x).encode())
		else:
			self.irc.send("PRIVMSG {} :.! No changes !.\r\n".format(self.channel).encode())

bot = IrcBot()
bot.main_loop()
