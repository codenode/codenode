import os

from django.core.management.base import NoArgsCommand

from twisted.scripts.twistd import ServerOptions, runApp
from twisted.application.app import run


def run(options):
    """ this reimplements twisted.application.app.run to use an option array, instead of argvs"""
    config = ServerOptions()
    try:
        config.parseOptions(options=options)
    except usage.error, ue:
        print config
        print "%s: %s" % (sys.argv[0], ue)
    else:
        runApp(config)


class Command(NoArgsCommand):
    """
    Run local desktop version of Codenode.  

    """

    def handle_noargs(self, **options):
        abspath = os.path.abspath(".")
        server_log = os.path.join(abspath, 'data', 'server.log')
        static_files = os.path.join(abspath, 'frontend', 'static')
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode "
        cmd += "--env_path=%s " % abspath
        cmd += "--server_log=%s " % server_log
        cmd += "--static_files=%s " % static_files
        run(cmd.split()[1:])