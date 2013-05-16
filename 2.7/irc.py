#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import irclib, ircbot
from functools import wraps

# In all these function, if value is not None, values must match themselves

def decorator_setattr(attr, value=None):
    """Set a flag to the decorated function"""
    def decorator(f):
        setattr(f, attr, value)
        return f
    return decorator

def dir_dict(o):
    """Return a dict `d` where `d.keys() == dir(o)` and `d.values` are the objectes pointed by"""
    return {e: getattr(o, e) for e in dir(o)}
    #return dict((e, getattr(o, e)) for e in dir(o))

def func_has_attr(f, attr, value=None):
    """Return True if `f` has attribute `attr`"""
    return (hasattr(f, attr) and (value is None or getattr(f, attr) == value))

def func_if_attr(f, attr, value=None, ret=(lambda *args: None)):
    """Return `f` if it has attribute `attr` else return `ret`"""
    return f if func_has_attr(f, attr, value) else ret

def all_funcs_with_attr(o, attr, value=None):
    """Return all objects from `o` with attribute `attr`"""
    return (f for f in dir_dict(o).values() if func_has_attr(f, attr, value))


"""
set_myattr = decorator_setattr('myattr')

class A:
    @set_myattr
    def toto(self):
        return 'func_toto'
    def tutu(self):
        return 'func_tutu'

a = A()                                                                                                          
print func_has_attr(a.toto, 'myattr')
print func_has_attr(a.tutu, 'myattr')

print func_if_attr(a.toto, 'myattr')()
print func_if_attr(a.tutu, 'myattr')()

for f in all_funcs_with_attr(a, 'myattr'):
    print f()
"""


welcome_hook = decorator_setattr('welcome_hook')
join_hook = decorator_setattr('join_hook')
part_hook = decorator_setattr('part_hook')
quit_hook = decorator_setattr('quit_hook')
pub_hook = decorator_setattr('pub_hook')
priv_hook = decorator_setattr('priv_hook')

class IRCBot(ircbot.SingleServerIRCBot, object):
    from collections import namedtuple
    Informations = namedtuple('Informations', ['chan', 'author', 'message', 'type'])

    def __init__(self, ircconfig):
        super(IRCBot, self).__init__(
        #ircbot.SingleServerIRCBot.__init__(self,
            [(ircconfig['server'], ircconfig.get('port', 6667))],
            ircconfig['nickname'],
            ircconfig['description']
        )
        self._connection_chan = ircconfig['chan']
        self._parent_process = ircconfig.get('parent_process', True)
        self._serv, self._ev = None, None
        self.current_infos = self.Informations('', '', '', '')

    def start(self, timeout=0.2):
        if self._parent_process:
            return super(IRCBot, self).start()
            #return ircbot.SingleServerIRCBot.start(self)
        self._connect()
        while True:
            try:
                self.ircobj.process_once(timeout)
            except Exception as e:
                print e

    def update_infos(self, serv, ev):
        self._serv, self._ev = serv, ev
        self.current_infos = self.Informations(
            ev.target(), # chan
            irclib.nm_to_n(ev.source()), # author
            ev.arguments()[0] if ev.arguments() else '', # message
            ev.eventtype()
        )

    def _current_infos_getter(attr):
        def getter(self):
            return getattr(self.current_infos, attr)
        return property(getter)
    chan    = _current_infos_getter('chan')
    author  = _current_infos_getter('author')
    message = _current_infos_getter('message')
    type    = _current_infos_getter('type')

    def annonce(self, *msgs):
        for msg in msgs:
            self._serv.privmsg(self._connection_chan, msg)
    def pub_response(self, msg, *msgs):
        self._serv.privmsg(self.chan, '%s: %s' % (self.author, msg))
        for msg in msgs:
            self._serv.privmsg(self.chan, msg)
    def priv_response(self, *msgs):
        for msg in msgs:
            self._serv.privmsg(self.author, msg)
    def notice(self, *msgs):
        for msg in msgs:
            self._serv.notice(self.author, msg)
    def response(self, *msgs):
        getattr(self, 'pub_response' if self.type == 'pubmsg' else 'priv_response')(*msgs)

    def on_welcome(self, serv, ev):
        if self._connection_chan:
            serv.join(self._connection_chan)

    def on_event(hook):
        def manager(self, *args):
            self.update_infos(*args)
            for f in all_funcs_with_attr(self, hook):
                f()
        return manager

    on_pubmsg = on_event('pub_hook')
    on_privmsg = on_event('priv_hook')
    on_join = on_event('join_hook')
    on_part = on_event('part_hook')
    on_quit = on_event('quit_hook')


pub_cmd = decorator_setattr('pub_cmd')
priv_cmd = decorator_setattr('priv_cmd')

class CommandsIRCBot(IRCBot):
    def on_cmd(cmd_hook):
        """If a message starts with `!xxx` and method `xxx` has attribute `cmd_hook`, this method will be called"""
        def manager(self):
            if self.message[0] == '!':
                action = self.message.split()
                cmd, args = action[0][1:], action[1:]
                try:
                    f = getattr(self, cmd, None)
                    if f:
                        func_if_attr(f, cmd_hook)(*args)
                except Exception as e:
                    print e
        return manager
    on_pub_cmd = pub_hook(on_cmd('pub_cmd'))
    on_priv_cmd = priv_hook(on_cmd('priv_cmd'))

    @pub_cmd
    @priv_cmd
    def help(self):
        """ : Displays this help page"""
        def append_cmds(l, attr):
            for f in all_funcs_with_attr(self, attr):
                l.append('!%s%s' % (f.__name__, f.__doc__ if f.__doc__ else ''))
        msgs = ['Commands available (public):']
        append_cmds(msgs, 'pub_cmd')
        msgs.append('privates:')
        append_cmds(msgs, 'priv_cmd')
        self.response(*msgs)


class UsersCommandsIRCBot(CommandsIRCBot):
    class NotRegistered(Exception):
        def __init__(self, username):
            super(UsersCommandsIRCBot.NotRegistered, self).__init__('user %s is not registered' % username)
            #Exception.__init__(self, 'user %s is not registered' % username)

    def __init__(self, ircconfig):
        super(UsersCommandsIRCBot, self).__init__(ircconfig)
        #CommandsIRCBot.__init__(self, ircconfig)
        self._register_password = ircconfig.get('register_password', '')
        self._users = set()
    @priv_cmd
    def register(self, password):
        """ password : Register request user if password is valid"""
        if self.author in self.channels[self._connection_chan].users():
            if password == self._register_password:
                self._users.add(self.author)
                self.notice('You are now registered')
            else:
                self.notice('Wrong password')
        else:
            self.notice('You have to be connected on chan %s' % self._connection_chan)
    @pub_cmd
    @priv_cmd
    def users(self):
        """ : Display registered users"""
        self.response(', '.join(self._users))
    @part_hook
    @quit_hook
    def disconnect_user(self):
        if self.author in self._users:
            self._users.remove(self.author)

def registered(old_f):
    @wraps(old_f)
    def f(self, *args, **kwargs):
        if self.author not in self._users:
            raise self.NotRegistered(self.author)
        return old_f(self, *args, **kwargs)
    return f


#class MyIRCBot(UsersCommandsIRCBot):
#    @pub_cmd
#    @priv_cmd
#    @registered
#    def tutu(self):
#        """ : test"""
#        self.response('Vous avez demandé "tutu", ne quittez pas')

import mpd
class MPDIRCBot(UsersCommandsIRCBot):
    def __init__(self, config):
        super(MPDIRCBot, self).__init__(config.irc)
        #UsersCommandsIRCBot.__init__(self, config.irc)
        self._mpdconfig = config.mpd
        self._mpd = mpd.MPDClient()
    def start(self):
        self._mpd.connect(
            self._mpdconfig.get('server', 'localhost'),
            self._mpdconfig.get('port', 6600),
        )
        if 'password' in self._mpdconfig:
            self._mpd.password(self._mpdconfig['password'])
        super(MPDIRCBot, self).start()
        #UsersCommandsIRCBot.start(self)

    @pub_cmd
    @priv_cmd
    def current(self):
        """ : Displays current song"""
        song = self._mpd.playlistinfo()[int(self._mpd.status()['songid'])]
        self.response(' - '.join((song['artist'], song['title'])))

    @pub_cmd
    @priv_cmd
    @registered
    def next(self):
        """ : Move to the next song (registered users only)"""
        self._mpd.next()
        self.notice('OK')

if __name__ == "__main__":
    from collections import namedtuple
    config = namedtuple('Config', ['irc', 'mpd'])({}, {})
    config.irc['nickname'] = 'irc_nick'
    config.irc['description'] = 'irc_descr'
    config.irc['server'] = 'irc_serv'
    config.irc['chan'] = 'irc_chan'
    #config.irc['parent_process'] = False
    config.irc['register_password'] = 'irc_users_passwd'
    config.mpd['password'] = 'mpd_passwd'
    bot = MPDIRCBot(config)
    bot.start()
