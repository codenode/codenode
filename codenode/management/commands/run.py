import os

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    """
    Run local desktop version of Codenode.  

    """

    def handle_noargs(self, **options):
        abspath = os.path.abspath(".")
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        server_log = os.path.join(abspath, 'data', 'server.log')
        static_files = os.path.join(abspath, 'frontend', 'static')
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode "
        cmd += "--env_path=%s " % abspath
        cmd += "--server_log=%s " % server_log
        cmd += "--static_files=%s " % static_files
        os.system(cmd)
