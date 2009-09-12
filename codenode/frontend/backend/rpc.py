
import xmlrpclib

def listEngineTypes(address):
    client = xmlrpclib.ServerProxy(address + '/admin/')
    engine_types = client.listEngineTypes()
    return engine_types

def allocateEngine(address, engine_type):
    client = xmlrpclib.ServerProxy(str(address) + '/admin/')
    access_id = client.allocateEngine(str(engine_type))
    return access_id

def interruptInstance(address, instance_id):
    client = xmlrpclib.ServerProxy(address + '/admin/')
    client.interruptInstance(instance_id)

