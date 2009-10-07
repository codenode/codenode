######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    notebook_opens_in_new_window = models.BooleanField(default=False)
    user = models.ForeignKey(User, unique=True)


