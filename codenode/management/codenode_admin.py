######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os
import shutil
import sys
import inspect
from functools import wraps

from django.core.management import call_command
from django.core.management.base import CommandError

import codenode
from codenode import management

CODE_PATH = os.path.abspath(os.path.dirname(codenode.__file__))
DESKTOP_ENV = os.path.join(os.path.expanduser("~"), '.codenode')
DEVEL_ENV = os.path.abspath(os.path.join(CODE_PATH, '..', 'devel', 'env'))


def setup_django(command):
    """ This decorator wraps an admin command to provide django setup.
    
    For standard development settings, use -devel flag. 
    For desktop settings use -desktop.
    For a django app, use '-settings mysite.settings'.
    Otherwise, pick up the settings from the cwd
    """
    @wraps(command)
    def wrapper(devel=False, desktop=False, settings=False, *args, **kwargs):
        
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
            
            envroot = os.getcwd()
            
            if devel: 
                envroot = DEVEL_ENV
                if not os.path.exists(envroot):
                    print 'development environment does not exist, '\
                        'please create with "codenode-admin init -desktop"'
                    sys.exit(1)
                
            elif desktop:
                envroot = DESKTOP_ENV          
                if not os.path.exists(envroot):
                    print 'desktop environment does not exist, '\
                        'please create with "codenode-admin init -devel"'
                    sys.exit(1)

            elif settings: 
                os.environ['DJANGO_SETTINGS_MODULE'] = settings

            else:
                if not os.path.exists(os.path.join('frontend', 'settings.py')):
                    print 'frontend.settings does not exists, please use inside a directory' \
                    ' created with "codenode-admin init dirname" or specify "-desktop" or "-devel"'
                    sys.exit(1)

            # make the django settings module importable and cd to it so spawned processes
            # can pick it up
            sys.path = [envroot] + sys.path
            os.chdir(envroot)
        
        # check the directory is good to go
        check_home_dir()
        
        # use devel_mode if we are running the devel env
        if devel and 'devel_mode' in inspect.getargspec(command)[0]:
            kwargs['devel_mode'] = True

        return command(*args, **kwargs)

    return wrapper
    
    
def build_twisted_cli(command, daemonize=False, devel_mode=False, pid_filename='codenode.pid'):
    """
    Build twisted incantation for a particular command
    """
    from django.conf import settings
    
    cmd = "twistd "
    if not daemonize:
        cmd += "-n "
    cmd += "--pidfile=%s " % os.path.join(settings.HOME_PATH, pid_filename)

    cmd += "%s " % command
    cmd += "--env_path=%s " % settings.HOME_PATH
    
    if command != 'codenode-backend':
        cmd += "--server_log=%s " % os.path.join(settings.HOME_PATH, 'server.log')
        cmd += "--static_files=%s " % settings.MEDIA_ROOT
        
        
    if devel_mode: 
        cmd += "--devel_mode "
        
    return cmd
    
    
def check_home_dir():
    """
    Check an environment directory contains a database and search index, etc. and required directories.
    """
    # non top level imports to prevent django settings setup before we have handled it
    from django.conf import settings
    from codenode.frontend.backend.fixtures.development import run as bootstrap_database
    from codenode.frontend.search import search
    
    for required_directory in [
            settings.HOME_PATH,
            settings.PLOT_IMAGES
        ]:
        if not os.path.exists(required_directory):
            os.mkdir(required_directory)
        
    if not os.path.exists(settings.DATABASE_NAME):
        call_command('syncdb', interactive=False)
        bootstrap_database()
        
    # a check for database schema version should go in here
    
    search.create_index()


def init_command(name=False, test=False, devel=False, desktop=False):
    """
    Initialize a codenode.

    Creates a new directory that will contain all needed
    sub-directories, config files, and other data to run
    an instance of codenode.
    
    Use the test flag to create a development environment
    where the code is symlinked.
    
    EXAMPLES:
        codenode-admin init -name mycodenode
        
        codenode-admin init -name mycodenode -test
    """
    
    osjoin = os.path.join
    copytree = shutil.copytree
    pkgroot = CODE_PATH
    settingstemplate = '_settings.py'
    
    if desktop: 
        envroot = DESKTOP_ENV
    elif devel: 
        envroot = DEVEL_ENV
        settingstemplate = '_devel_settings.py'
        test = True
    else:     
        abspath = os.path.abspath(".")
        envroot = osjoin(abspath, name)

    if os.path.exists(envroot):
        print 'target directory (%s) already exists, exiting...' % envroot
        sys.exit(1)
    os.mkdir(envroot)
    
    if test:
        # for test environments we symlink to the code rather than copy
        try: 
            copytree = os.symlink
        except AttributeError:
            pass   

    for dir in ["frontend", "backend"]:
        os.makedirs(osjoin(envroot, dir))
        open(osjoin(osjoin(envroot, dir), "__init__.py"), "w").close()
        settingsfile = osjoin(osjoin(pkgroot, dir), settingstemplate)
        shutil.copyfile(settingsfile,  osjoin(osjoin(envroot, dir), "settings.py"))

    for dir in ["static", "templates"]:
        dirroot = osjoin("frontend", dir)
        pkgdirroot = osjoin(pkgroot, dirroot)
        copytree(pkgdirroot, osjoin(envroot, dirroot))

    pkgdataroot = osjoin(pkgroot, "data")
    copytree(pkgdataroot, osjoin(envroot, "data"))

    pkgtwistedroot = osjoin(pkgroot, "twisted")
    copytree(pkgtwistedroot, osjoin(envroot, "twisted"))


@setup_django
def run_command(daemonize=False): #, frontendpid=None):
    """
    Run local desktop version of Codenode.  
    Use inside a directory created with "codenode-admin init".

    """
    os.system(build_twisted_cli('codenode', daemonize))


@setup_django
def frontend_command(daemonize=False, devel_mode=False):
    """
    Run the Frontend server.
    """
    os.system(build_twisted_cli('codenode-frontend', 
                                daemonize, devel_mode, pid_filename='frontend.pid'))


@setup_django
def backend_command(daemonize=False, devel_mode=False):
    """
    Run a Backend Server.
    """
    os.system(build_twisted_cli('codenode-backend', 
                                daemonize, devel_mode, pid_filename='backend.pid'))


@setup_django
def syncdb_command():
    """
    Run Django's `syncdb`.
    """
    call_comand('syncdb', interactive=False)


@setup_django
def bootstrapdb_command():
    """
    Load default codenode setup: an admin user, and a local backend with a python engine.
    """
    from codenode.frontend.backend.fixtures.development import run as bootstrap_database
    bootstrap_database()


@setup_django
def dbshell_command():
    """
    Database shell
    """
    call_command('dbshell')


@setup_django
def shell_command():
    """
    Open a python shell.
    """
    try:
        call_command('shell_plus')
    except CommandError:
        call_command('shell')
        
@setup_django
def resetdb_command():
    """
    Open a database shell.
    """
    call_command('reset_db')
    call_command('syncdb', interactive=False)
    from codenode.frontend.backend.fixtures.development import run as bootstrap_database
    bootstrap_database()
        

def backendmanhole_command():
    """
    Open a manhole to the backend.
    """
    # TODO: pick up port from configuration
    os.system('telnet localhost 6024')


def frontendmanhole_command():
    """ 
    Open a manhole to the frontend.
    """
    # TODO: pick up port from configuration
    os.system('telnet localhost 6023')
    
        
def help_command(**options):
    """
    Prints out help for the commands. 

    codenode-admin help

    You can get help for one command with:

    codenode-admin help -for start
    """
    if "for" in options:
        help = management.args.help_for_command(management.codenode_admin, options['for'])
        if help:
            print help
        else:
            management.args.invalid_command_message(management.codenode_admin, exit_on_error=True)
    else:
        print "codenode-admin help:\n"
        print "\n".join(management.args.available_help(management.codenode_admin))

