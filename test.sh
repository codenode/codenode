#!/bin/bash
export DJANGO_SETTINGS_MODULE=frontend._settings
django-admin.py test --pythonpath codenode --exclude="compress|twisted" $@
