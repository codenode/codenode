from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    notebook_opens_in_new_window = models.BooleanField(default=False)
    user = models.ForeignKey(User, unique=True)


