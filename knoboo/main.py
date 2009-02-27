##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 
"""
Main services provided by the knoboo distribution.

"""
import os
import knoboo
k_path = knoboo.__path__[0]

from django.core.management import setup_environ
from knoboo import settings
settings_path = setup_environ(settings)

from twisted.application import internet, service, strports
from twisted.cred import portal, checkers, credentials
from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.runner.procmon import ProcessMonitor


from knoboo.external.twisted.web2 import log, server, channel

from knoboo.kernel.interface import KernelClientManager
from knoboo.kernel.server import KernelManagerRealm
from knoboo.kernel.procman import ProcessManager

class InMemoryPasswordDatabase(checkers.InMemoryUsernamePasswordDatabaseDontUse):
    """This is used for authenticating kernel connections.
    It is a temporary solution that needs a little more... 
    """

    def requestAvatarId(self, credentials):
        return defer.maybeDeferred(
                credentials.checkPassword, 
                self.users['user1']).addCallback(
                self._cbPasswordMatch, str(credentials.username))


def desktopService(config):
    from knoboo.resources import avatars, notebook
    from knoboo.authority import guard, check

    db = config.db['main_path']
    if not os.path.exists(db):
        manager.Database('sqlite:///' + db)
    dbManager = manager.DatabaseManager('sqlite:///' + config.db['main_path'])

    nbSessionManager = notebook.SessionManager(dbManager, config)

    kservice = service.MultiService()

    if config.kernel['kernel_host'] == 'localhost':
        procman = ProcessManager()
        procman.setServiceParent(kservice)
        kernel = KernelClientManager(config, procman)
        kernel.start()

    realm = avatars.LoginSystem(dbManager, nbSessionManager, config)
    p = portal.Portal(realm)
    p.registerChecker(check.NewHashedPasswordDataBaseChecker(dbManager))
    p.registerChecker(checkers.AllowAnonymousAccess(), credentials.IAnonymous)

    rsrc = guard.SessionWrapper(p)

    site = server.Site(rsrc)
    factory = channel.HTTPFactory(site)

    d = 'tcp:%s' % config.server['port']
    srv = strports.service(d, factory)
    srv.setServiceParent(kservice)

    if config['open_browser']:
        import webbrowser
        url = 'http://localhost:%s' % config.server['port']
        reactor.callWhenRunning(webbrowser.open_new, url)

    return kservice



def webService(config):
    from knoboo.async.resources import UserNotebooks
    from knoboo.async.resources import SessionManager


    nbSessionManager = SessionManager()

    kservice = service.MultiService()

    procmonitor = ProcessMonitor()
    procmonitor.setServiceParent(kservice)
    django_frontend_args = [
            'python',
            os.path.join(k_path, 'manage.py'),
            'runserver',
            '8001',
            ]
    #procmonitor.addProcess('django_frontend', django_frontend_args)


    if config.kernel['kernel_host'] == 'localhost':
        procman = ProcessManager()
        procman.setServiceParent(kservice)
        kernel = KernelClientManager(config, procman)
        kernel.start()

    


    rsrc = UserNotebooks(nbSessionManager)
    if config.server['host'] != 'localhost':
        from knoboo.external.twisted.web2 import vhost
        rsrc = vhost.VHostURIRewrite(config.server['host'], rsrc)

    #rsrc = log.LogWrapperResource(rsrc) #XXX This enable verbose http logging.
    #log.DefaultCommonAccessLoggingObserver().start()

    site = server.Site(rsrc)
    factory = channel.HTTPFactory(site)


    if config.server['proxy']:
        # backend server behind apache or nginx
        d = 'tcp:%s:interface=127.0.0.1' % config.server['port']
        srv = strports.service(d, factory)
        srv.setServiceParent(kservice)
    else:
        d = 'tcp:%s' % config.server['port']
        srv = strports.service(d, factory)
        srv.setServiceParent(kservice)
            
    return kservice
 


def kernelService(config):
    kservice = service.MultiService()

    procman = ProcessManager()
    procman.setServiceParent(kservice)

    engines_max = int(config['engines-max'])
    if  engines_max > 1:
        from knoboo.kernel.interface import UserPool
        prefix = config['engines-user-prefix']
        group = config['engines-group']
        user_pool = UserPool(engines_max, prefix, group)
    else:
        user_pool = None

    realm = KernelManagerRealm(config, procman, user_pool)
    p = portal.Portal(realm)
    #chk= checkers.InMemoryUsernamePasswordDatabaseDontUse(user1="secret")
    chk= InMemoryPasswordDatabase(user1="secret")
    p.registerChecker(chk)
    srv = internet.TCPServer(int(config['port']), pb.PBServerFactory(p))
    srv.setServiceParent(kservice)
    return kservice













