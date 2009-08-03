
import xmlrpclib

def listEngineTypes(address):
    client = xmlrpclib.ServerProxy(address + '/admin/')
    engine_types = client.listEngineTypes()
    return engine_types

def runEngineInstance(address, engine_type):
    client = xmlrpclib.ServerProxy(address + '/admin/')
    engine_id = client.runEngineInstance(engine_type)
    return engine_id
