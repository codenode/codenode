import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
from codenode import service

desktop = service.DesktopServiceMaker()
frontend = service.FrontendServiceMaker()
