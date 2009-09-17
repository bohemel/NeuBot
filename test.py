#!/usr/bin/env python
from controllers import IRCController
from controllers import EventController

from lib.logger import Logger

from models import Channel
from models import Server

import time

class NeuerBot:
	def __init__(self, config):
		self.config = config
		self.eventcontroller = EventController()

		self.irccontrollers = []

	def start(self):
		botconfig = self.config.Bot

		for net in botconfig['ircnets']:
			irc = IRCController(self.eventcontroller)

			# Add channels
			for (channel_name, channel_key) in net['channels']:
				channel = Channel(channel_name, channel_key)
				irc.channels.append(channel)

			# Add servers
			if len(net['servers']) == 0: raise Exception("There must be at least one server defined")

			for (hostname, port, use_ssl, use_ipv6) in net['servers']:
				server = Server(hostname, port, use_ssl, use_ipv6)
				irc.servers.append(server)

			irc.ircnet   = net['ircnet']
			irc.nick     = net['nick']
			irc.altnicks = net['altnicks']
			irc.name     = net['name']
			irc.ident    = net['ident']

			Logger.Info("Connecting to %s..." % irc.ircnet)
			irc.connect()

			self.irccontrollers.append(irc)

	def stop(self):
		for irc in self.irccontrollers:
			irc.disconnect()

if __name__ == "__main__":
	try:
		Logger.EnableDebug()
		Logger.Info("Initializing...")
		import Config

		bot = NeuerBot(Config)
		bot.start()

		while True:
			# Perform stuff
			time.sleep(1)

	except KeyboardInterrupt:
		Logger.Info("Keyboard interrupt detected. Shutting down.")
		import rpdb2
		rpdb2.start_embedded_debugger("foobar")
		#bot.stop()

	except Exception, e:
		Logger.Fatal("Fatal error: %s" % e)
		bot.stop()
