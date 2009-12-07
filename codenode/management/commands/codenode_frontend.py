import os

from django.core.management.base import NoArgsCommand
from django.conf import settings 

from codenode_desktop import run

class Command(NoArgsCommand):
    """
    Run the Frontend server.
    """

    def handle_noargs(self, **options):
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode-frontend "
        cmd += "--env_path=%s " % settings.HOME_PATH
        cmd += "--server_log=%s " % os.path.join(settings.HOME_PATH, 'server.log')
        cmd += "--static_files=%s " % os.path.join(settings.PROJECT_PATH, 'static')
        run(cmd.split()[1:])
            
        run(cmd.split()[1:])