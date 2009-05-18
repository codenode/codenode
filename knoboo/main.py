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

from django.core.management import setup_environ
from knoboo import settings
settings_path = setup_environ(settings)

from twisted.application import internet, service, strports
from twisted.cred import portal, checkers, credentials
from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.runner.procmon import ProcessMonitor


from knoboo.kernel.interface import KernelClientManager
from knoboo.kernel.server import KernelManagerRealm
from knoboo.kernel.procman import ProcessManager


class Config(object):
    kernel = {}
    database = {}
    server = {}

class KernelConfig(dict):
    dconfig = {"python":"/usr/bin/python"}


def webService():
    from knoboo.async.webresources import Notebook
    from knoboo.async.webresources import SessionManager
    
    """
    procmon_service = ProcessMonitor()
    """
    procman = ProcessManager()

    #XXX the below configuration hacks will be pulled
    # out and turn into a combination of:
    # Twisted Plugin and Django settings usage.
    config = Config()
    config.kernel["kernel_path"] = os.path.abspath(".")+"data"
    config.kernel["kernel_host"] = "localhost"
    config.kernel["kernel_port"] = "8337"

    kernel_config = KernelConfig()
    enginepath = os.path.join(os.path.abspath("."), "data")
    kernel_config.update({"port":8337, "engines-uid":"None", "engines-max":1, "engines-path":enginepath, 
        "engines-root":enginepath, "engines-pythonpath":enginepath})
    kernel_server_service = kernelService(kernel_config)

    kernel = KernelClientManager(config, procman)
    kernel.start()

    nbSessionManager = SessionManager()
    kernel_web_rsrc = Notebook(nbSessionManager)
    return kernel_web_rsrc, kernel_server_service




class InMemoryPasswordDatabase(checkers.InMemoryUsernamePasswordDatabaseDontUse):
    """This is used for authenticating kernel connections.
    It is a temporary solution that needs a little more... 
    """

    def requestAvatarId(self, credentials):
        return defer.maybeDeferred(
                credentials.checkPassword, 
                self.users['user1']).addCallback(
                self._cbPasswordMatch, str(credentials.username))

def kernelService(config):
    kservice = service.MultiService()

    procman = ProcessManager()
    procman.setServiceParent(kservice)

    engines_max = 0 #int(config['engines-max'])
    if engines_max > 1:
        from knoboo.kernel.interface import UserPool
        prefix = config['engines-user-prefix']
        group = config['engines-group']
        user_pool = UserPool(engines_max, prefix, group)
    else:
        user_pool = None

    realm = KernelManagerRealm(config, procman, user_pool)
    p = portal.Portal(realm)
    chk = InMemoryPasswordDatabase(user1="secret")
    p.registerChecker(chk)
    srv = internet.TCPServer(int(config['port']), pb.PBServerFactory(p))
    srv.setServiceParent(kservice)
    return kservice

