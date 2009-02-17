##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 

from twisted.application import service

from knoboo.main import webService
from knoboo.config import ServerOptions

config = ServerOptions()
config.parseConfigFile()

ser = webService(config)
application = service.Application('knoboo')
ser.setServiceParent(service.IServiceCollection(application))

