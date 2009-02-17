##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 

from twisted.application import service

from twisted.cred import portal, checkers, credentials
from twisted.spread import pb

from knoboo.main import kernelService
from knoboo.config import KernelServerOptions

config = KernelServerOptions()
config.parseConfigFile()

ser = kernelService(config)
application = service.Application('knoboo-kernel')
ser.setServiceParent(service.IServiceCollection(application))

