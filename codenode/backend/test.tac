from twisted.application import service

from codenode.backend.core import makeServices

backendServices = makeServices()

application = service.Application('backend')
backendServices.setServiceParent(application)
