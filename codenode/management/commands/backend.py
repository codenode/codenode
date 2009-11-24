import os

from django.core.management.base import NoArgsCommand

from run import run


class Command(NoArgsCommand):
    """
    Run a Backend Server.
    """

    def handle_noargs(self, **options):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        abspath = os.path.abspath(".")
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode-backend "
        cmd += "--env_path=%s " % abspath
        run(cmd.split()[1:])