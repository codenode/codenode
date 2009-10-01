import os 
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.frontend.settings'

from django.contrib.auth.models import User
from django.db import connection
from django.core.management import call_command

import settings



def setup():
    """This is a package level setup that gets called by nose to setup Django databases
        
    Django has some test utils that do all this, but since we don't have an accessible 
    manage.py or settings.py, it is tricky to get them to run.  Instead, we'll just call
    a database sync here.
    
    Also, create a user that we can use in the tests
    """
    
    if os.path.exists(settings.DATABASE_NAME):
        os.remove(settings.DATABASE_NAME)
    
    call_command("syncdb")

    for user in [User(username='test'), User(username='test2')]:
        user.set_password('password')
        user.save()
        
