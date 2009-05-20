import os
import sys
sys.path.append('knoboo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'knoboo.settings'

from knoboo import service

knoboo_desktop = service.DesktopServiceMaker()
knobood_web_app = service.WebAppServiceMaker()
knoboo_kernel = service.KernelServerServiceMaker()
