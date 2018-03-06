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

		print("[+] Connecting to {}".format(server))
		self.irc.connect((server, 6667)) # connect to server

		# Authenticate
		self.irc.send("NICK {}\n".format(botnick).encode())
		self.irc.send("USER {} 8 * :{}\n".format(botnick, "Dobry bot do wrzucania zmian ;;;;").encode())
		self.irc.send("JOIN {}\n".format(channel).encode())

		print("[+] Connected to {}".format(server))


	def main_loop():
		while 1:
			text = irc.recv(2048).decode()
			# Optional logging ig someting breaks
			# print("[*] Received: {}".format(text))

			# Various commands
			# More to come ofc
			if "PING" in text:
				print("\n\t[!] Received PING. Sending response to server.\n")
				irc.send("PONG {}\r\n".format(text.split()[1]).encode())
				print("\n\t[!] Sent PONG.\n")

			elif "!changes" in text:
				irc.send("PRIVMSG {} :Fetching...\r\n".format(channel).encode())
				chg = changes.Changes().irc_changes()
				irc.send("PRIVMSG {} :Here you go:\r\n".format(channel).encode())
				if chg:
					for line in chg:
						irc.send("PRIVMSG {} :{}\r\n".format(channel, line[0]).encode())
						for x in line[1:]:
							irc.send("PRIVMSG {} :    {}\r\n".format(channel, x).encode())
				else:
					irc.send("PRIVMSG {} :!! No changes !!\r\n".format(channel).encode())
