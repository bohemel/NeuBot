class IRCMessageController:
	def __init__(self, irccontroller, ircmessage):
		self.server = irccontroller
		self.message = ircmessage

	def reply(self, message):
		if self.server.nick == self.message.destination:
			self.server.privmsg(self.message.source.nick, message)
		else:
			self.server.privmsg(self.message.destination, message)

	def reply_notice(self, message):
		self.server.notice(self.message.destination, message)

	def __getattr__(self, attr):
		# Delegate methods to the IRCController
		return getattr(self.server, attr)
		
