#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# ./manage.py dumpscript

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def run():
    
    from django.contrib.auth.models import User
    
    auth_user_1 = User()
    auth_user_1.username = u'admin'
    auth_user_1.first_name = u''
    auth_user_1.last_name = u''
    auth_user_1.email = u'admin@example.com'
    auth_user_1.password = u'sha1$5dbb9$8ba5bd30d0826b8eae5cbf76ae88b19f934aeca1'
    auth_user_1.is_staff = True
    auth_user_1.is_active = True
    auth_user_1.is_superuser = True
    auth_user_1.last_login = datetime.datetime(2009, 10, 17, 8, 56, 0, 458130)
    auth_user_1.date_joined = datetime.datetime(2009, 10, 17, 8, 54, 47, 894137)
    auth_user_1.save()

    from codenode.frontend.backend.models import BackendServer

    backend_backendserver_1 = BackendServer()
    backend_backendserver_1.name = u'local'
    backend_backendserver_1.address = u'http://localhost:8337'
    backend_backendserver_1.save()

    from codenode.frontend.backend.models import EngineType

    backend_enginetype_1 = EngineType()
    backend_enginetype_1.name = u'Python'
    backend_enginetype_1.backend = backend_backendserver_1
    backend_enginetype_1.description = None
    backend_enginetype_1.save()

    print '-' * 80
    print "'admin' user created with password 'admin'."
    print "Local backend server on port 8337 declared with a python backend."
    print '-' * 80
    
    