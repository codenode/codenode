import os

from django.core.management.base import NoArgsCommand

from codenode_desktop import run

class Command(NoArgsCommand):
    """
    Run the Frontend server.
    """

    def handle_noargs(self, **options):
        abspath = os.path.abspath(env_path)
        server_log = os.path.join(abspath, 'data', 'server.log')
        static_files = os.path.join(abspath, 'frontend', 'static')
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode-frontend "
        cmd += "--env_path=%s " % abspath
        cmd += "--server_log=%s " % server_log
        cmd += "--static_files=%s " % static_files
            
        run(cmd.split()[1:])