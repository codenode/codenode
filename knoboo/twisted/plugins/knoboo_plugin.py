import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
from knoboo import service

knoboo_desktop = service.DesktopServiceMaker()
knobood_web_app = service.WebAppServiceMaker()
knoboo_kernel = service.KernelServerServiceMaker()
