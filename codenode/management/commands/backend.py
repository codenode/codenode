import os

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    """
    Run a Backend Server.
    """

    def handle_noargs(self, **options):
        abspath = os.path.abspath(".")
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode-backend "
        cmd += "--env_path=%s " % abspath
        os.system(cmd)
