# -*- coding: utf-8 -*-
__module_class_names__ = ["RememberSaying", "SaySaying","RememberYT","SayYT","Dump"]

from bot import Module
from admin import is_authorised
import pickle, re, os.path
import random
import logging

logger = logging.getLogger(__name__)

FNAME_S = os.path.expanduser('~/.ircbot/modulefiles/parrot_sayings.pickle')
FNAME_Y = os.path.expanduser('~/.ircbot/modulefiles/parrot_yt_links.pickle')
CHANCES = (6,2,10) # (remember,say,thank)
CHOICES = (
        "I love you!",
        "<3",
        ":*",
        "you know that I know..."
        )
sayings = list()
yt_links = list()

class RememberSaying(Module):
    def __init__(self, bot, config):
        Module.__init__(self, bot, config)
        self.config["threadable"] = True
        self.config["thread_timeout"] = 1.0
        self.handler_type = "privmsg"
        self.rule = r'.*?(?:[a-zA-Z0-9_.,=?-]+?[:,])? *(.*)'
        global sayings 
        try:
            sayings = pickle.Unpickler(open(FNAME_S,'rb')).load()
        except IOError:
            sayings = list()
            pickle.Pickler(open(FNAME_S,'wb')).dump(sayings)

    def run(self, bot, params):
        if random.randint(1,100)>CHANCES[0]:
            return
        regexp = r'.*(https?\://).*'
        if re.match(regexp,bot.line):
            return
        regexp = r'[.-_/\\].*'
        if re.match(regexp,bot.line):
            return
        global sayings 
        saying = bot.match.groups()[0]
        sayings.append(saying)
        pickle.Pickler(open(FNAME_S,'wb')).dump(sayings)
        if random.randint(1,100)<=CHANCES[2]:
            bot.say(bot.target, "Remembered!")
            return
        if random.randint(1,100)>CHANCES[1]:
            return
        bot.say(bot.target,bot.sender.split("!")[0] + ": " + random.choice(CHOICES))

class SaySaying(Module):
    def __init__(self, bot, config):
        Module.__init__(self, bot, config)
        self.handler_type = "privmsg"
        self.rule = r'([a-zA-Z0-9_.,=?-]+?[:,])?.*'
        global sayings
        try:
            sayings = pickle.Unpickler(open(FNAME_S,'rb')).load()
        except IOError:
            sayings = list()
            pickle.Pickler(open(FNAME_S,'wb')).dump(sayings)

    def run(self, bot, params):
        modifier = (bot.match.group(0) and (bot.config["nick"] in bot.match.group(0))) and 34 or 0
        if random.randint(1,100)>(CHANCES[1]+modifier):
            return
        global sayings 
        if sayings:
            bot.say(bot.target, bot.sender.split("!")[0] + ": " + random.choice(sayings))

class RememberYT(Module):
    def __init__(self, bot, config):
        Module.__init__(self, bot, config)
        self.config["threadable"] = True
        self.config["thread_timeout"] = 1.0
        self.handler_type = "privmsg"
        self.rule = r'.*(http\://[a-z0-9]+\.youtube\.[a-z]+/watch\?v=[a-zA-Z0-9\-_\+\,\.]+)\&?.*'
        global yt_links
        try:
            yt_links = pickle.Unpickler(open(FNAME_Y,'rb')).load()
        except IOError:
            yt_links = list()
            pickle.Pickler(open(FNAME_Y,'wb')).dump(yt_links)

    def run(self, bot, params):
        global yt_links
        if not bot.match.group(1) in yt_links:
            yt_links.append(bot.match.group(1))
            pickle.Pickler(open(FNAME_Y,'wb')).dump(yt_links)
        else: return
        if random.randint(1,100)>CHANCES[2]:
            return
        choices = ("I love you!","<3",":*",
                "you know that I know...",
                "stupido!","tell me about it",
                "I bet you don't know what is going to happen next...")
        bot.say(bot.target, bot.sender.split("!")[0] + ": " + random.choice(choices))

class SayYT(Module):
    def __init__(self, bot, config):
        Module.__init__(self, bot, config)
        self.config["threadable"] = True
        self.config["thread_timeout"] = 1.0
        self.handler_type = "privmsg"
        self.rule = r'%s[:,].*?(link|jutub|tube|film).*' % bot.config["nick"]
        global yt_links
        try:
            yt_links = pickle.Unpickler(open(FNAME_Y,'rb')).load()
        except EOFError:
            yt_links = list()
            pickle.Pickler(open(FNAME_Y,'wb')).dump(yt_links)

    def run(self, bot, params):
        global yt_links
        if not yt_links:
            bot.say(bot.target, bot.sender.split("!")[0] + ": sorry, don't know any...")
            return
        bot.say(bot.target, bot.sender.split("!")[0] + ": " + random.choice(yt_links))

class Dump(Module):
    def __init__(self, bot, config):
        Module.__init__(self, bot, config)
        self.config["threadable"] = True
        self.config["thread_timeout"] = 1.0
        self.handler_type = "privmsg"
        self.rule = r'\.dump'
    
    def run(self, bot, params):
        if not is_authorised(bot.sender):
            logger.warn("Unauthorized attempt to dump the database")
            return
        global sayings
        global yt_links
        logger.info("yt_links:")
        for x in yt_links:
            logger.info("%s", x)
        logger.info("sayings:")
        for x in sayings:
            logger.info("%s", x)
