import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
from codenode import service

codenode_desktop = service.DesktopServiceMaker()
codenoded_web_app = service.WebAppServiceMaker()
codenode_kernel = service.KernelServerServiceMaker()
