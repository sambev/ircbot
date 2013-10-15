"""
Al - for Alan Turing

If someone says the bot's name in the channel followed by a ':',
e.g.

    <sam> al: hello!

the al will reply:

    <logbot> sam: I am AL

Run this script with four arguments:
e.g.
    <server/ip>:    'irc.freenode.net'
    <port>:         6667
    <channel>:      main
    <logfile>:      log/channel.log

    $ python AL.py irc.freenode.net 6667 main log/channel.log
"""


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys
from scrapers.cafescraper import scrapeCafe
from apis.weatherman import currentWeather
from apis.wolfram import wolfram
from apis.urbandic import urbandic
import ConfigParser


class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file


    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()


    def close(self):
        self.file.close()



class LogBot(irc.IRCClient):
    """A logging IRC bot."""
   
    # the nickname might have problems with uniquness when connecting to freenode.net 
    nickname = "AL"
    __stored_messages = {} # used for user messages with the tell command
    __points = {}
    

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.join(self.factory.channel)


    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)


    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)


    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        parts = msg.split()
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # if someone is trying to give points
        if parts[0][-2:] == '++':
            user = parts[0][:-2]
            if user[-1] == ':':  # if the user has ':' with their name from autocomplete
                user = user[:-1]
            # if the user is already in the dictionary
            if user in self.__points:
                    self.__points[user] += 1
            # if they aren't being recorded yet, start them at 1 or -1
            else:
                    self.__points[user] = 1

            if self.__points[user] == 1:
                self.msg(channel, '{0} has {1} point'. format(user, self.__points[user]))
            else:
                self.msg(channel, '{0} has {1} points'. format(user, self.__points[user]))


        #==========================================================================================
        # ---------- MESSAGES DIRECTED AT ME
        #==========================================================================================
        if parts[0] == self.nickname + ':':
            if parts[1] == 'cafe':
                try:
                    menu = scrapeCafe()
                    # make the menu all nice for chat purposes
                    menu_msg = 'Steam \'n Turren: {0}.\nField of Greens:{1}.\
                        \nFlavor & Fire: {2}.\nThe Grillery: {3}.\
                        \nMain Event: {4}'.format(
                                            menu['soup'], 
                                            menu['greens'], 
                                            menu['flavor'], 
                                            menu['grill'], 
                                            menu['main'])
                    self.msg(channel, menu_msg)
                    self.logger.log(menu_msg)
                except Exception as e:
                    print e.message
                    self.msg(channel, 'Sorry, I do not understand')
                    pass

            elif parts[1] == 'weather':
                try:
                    # get the weather and tell the channel
                    weather = currentWeather()
                    w_msg = '{0},  {1} degrees'.format(weather['status'], weather['temp'])
                    self.msg(channel, w_msg)
                    self.logger.log(w_msg)
                except Exception as e:
                    print e.message
                    self.msg(channel, 'Sorry I do not understand')
                    pass

            elif parts[1] == 'tell':
                try:
                    # form the message
                    target_user = parts[2]
                    tell_msg = '{0}, {1} said: {2}'.format(target_user, user, ' '.join(parts[3:]))
                    if target_user not in self.__stored_messages:
                        self.__stored_messages[target_user] = []
                    self.__stored_messages[target_user].append(tell_msg)
                    self.msg(channel, 'I will pass that along when {0} joins'.format(target_user))
                except Exception as e:
                    print e.message
                    self.msg(channel, 'Give me a message to tell someone!: `AL: tell <user> <message>`')

            elif parts[1] == 'help':
                try:
                    help_msg = 'I currently support the following commands:\
                    \ncafe\nweather\n\
                    \ntell <user> <message>'
                    self.msg(channel, help_msg)
                except Exception as e:
                    print e.message
                    self.msg(channel, 'The help command broke')

        #==========================================================================================
        # ---------- IF NOT ONE OF THE SPECIAL COMMANDS ABOVE ASK WOLFRAM
        #==========================================================================================
            else:
                try:
                    config = ConfigParser.RawConfigParser()
                    config.read('wfconfig.cfg')
                    key = config.get('wolfram', 'key')
                    question = ' '.join(parts[1:])
                    w = wolfram(key)
                    answer = w.search(question)
                    if not answer:                        
                        urban_response = urbandic(question)
                        if urban_response:
                            answer = '{0} \nFor Example: {1}\n{2}'.format(
                                                urban_response['definition'], 
                                                urban_response['example'], 
                                                urban_response['permalink']) 
                        else:
                            answer = 'i don\'t know'
                    self.msg(channel, answer)
                except Exception as e:
                    print e
                    print 'I died trying to ask wolfram a question'


    def userJoined(self, user, channel):
        """This will get called when I see a user join a channel"""
        #check to see if I need to tell anyone anything
        try:
            if user in self.__stored_messages:
                for message in self.__stored_messages[user]:
                    self.msg(channel, message)
                #remove the messages
                del self.__stored_messages[user]           
        except Exception as e:
            print e
            self.msg(channel, 'I was trying to tell someone something, but I broke. :(')


    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))


    # irc callbacks
    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    f = LogBotFactory(sys.argv[3], sys.argv[4])

    # connect factory to this host and port
    reactor.connectTCP(sys.argv[1], int(sys.argv[2]), f)

    # run bot
    reactor.run()
