import os

from django.core.management import call_command
from django.core.management.base import NoArgsCommand
from django.conf import settings 

from twisted.scripts.twistd import ServerOptions, runApp
from twisted.application.app import run

from codenode.frontend.backend.fixtures.development import run as bootstrap_database
from codenode.frontend.search import search


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
    
    def check_home_dir(self, path):
        """ check an environment directory contains a database and search index, etc."""
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        if not os.path.exists(settings.DATABASE_NAME):
            call_command('syncdb', interactive=False)
            bootstrap_database()
            
        # a check for database schema version should go in here
        
        search.create_index()
        

    def handle_noargs(self, **options):
        self.check_home_dir(settings.HOME_PATH)
        cmd = "twistd "
        if not options.get('daemonize', False):
            cmd += "-n "
        cmd += "codenode "
        cmd += "--env_path=%s " % settings.HOME_PATH
        cmd += "--server_log=%s " % os.path.join(settings.HOME_PATH, 'server.log')
        cmd += "--static_files=%s " % os.path.join(settings.PROJECT_PATH, 'static')
        run(cmd.split()[1:])