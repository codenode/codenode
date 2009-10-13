######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os
import shutil

import codenode
from codenode import management


def init_command(name=None):
    """
    Initialize a codenode.

    Creates a new directory that will contain all needed
    sub-directories, config files, and other data to run
    an instance of codenode.
    
    EXAMPLES:
        codenode-admin init -name mycodenode
    """
    osjoin = os.path.join
    abspath = os.path.abspath(".")
    envroot = osjoin(abspath, name)
    pkgroot = os.sep.join(codenode.__file__.split(os.sep)[:-1])
    os.mkdir(envroot)
    for dir in ["frontend", "backend"]:
        os.makedirs(osjoin(envroot, dir))
        open(osjoin(osjoin(envroot, dir), "__init__.py"), "w").close()
        settingsfile = osjoin(osjoin(pkgroot, dir), "_settings.py")
        shutil.copyfile(settingsfile,  osjoin(osjoin(envroot, dir), "settings.py"))

    for dir in ["static", "templates", "compress"]:
        dirroot = osjoin("frontend", dir)
        pkgdirroot = osjoin(pkgroot, dirroot)
        shutil.copytree(pkgdirroot, osjoin(envroot, dirroot))

    pkgdataroot = osjoin(pkgroot, "data")
    shutil.copytree(pkgdataroot, osjoin(envroot, "data"))

    pkgtwistedroot = osjoin(pkgroot, "twisted")
    shutil.copytree(pkgtwistedroot, osjoin(envroot, "twisted"))


def run_command(daemonize=False): #, frontendpid=None):
    """
    Run local desktop version of Codenode.  
    Use inside a directory created with "codenode-admin init".

    """
    abspath = os.path.abspath(".")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
    server_log = os.path.join(abspath, 'data', 'server.log')
    static_files = os.path.join(abspath, 'frontend', 'static')
    cmd = "twistd "
    if not daemonize:
        cmd += "-n "
    cmd += "codenode "
    cmd += "--env_path=%s " % abspath
    cmd += "--server_log=%s " % server_log
    cmd += "--static_files=%s " % static_files
    os.system(cmd)

def frontend_command(daemonize=False, env_path='.', devel=False):
    """
    Run the Frontend server.
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
    abspath = os.path.abspath(env_path)
    server_log = os.path.join(abspath, 'data', 'server.log')
    static_files = os.path.join(abspath, 'frontend', 'static')
    cmd = "twistd "
    if not daemonize:
        cmd += "-n "
    cmd += "codenode-frontend "
    cmd += "--env_path=%s " % abspath
    cmd += "--server_log=%s " % server_log
    cmd += "--static_files=%s " % static_files
    os.system(cmd)


def backend_command(daemonize=False):
    """
    Run a Backend Server.
    """
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
    abspath = os.path.abspath(".")
    cmd = "twistd "
    if not daemonize:
        cmd += "-n "
    cmd += "codenode-backend "
    cmd += "--env_path=%s " % abspath
    os.system(cmd)

def syncdb_command():
    """
    Run Django's `syncdb`.
    """
    #from django.core.management import call_command
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
    #call_command("syncdb")
    os.system('django-admin.py syncdb --pythonpath="." --settings="frontend.settings"')


def help_command(**options):
    """
    Prints out help for the commands. 

    codenode-admin help

    You can get help for one command with:

    codenode-admin help -for start
    """
    if "for" in options:
        help = management.args.help_for_command(management.commands, options['for'])
        if help:
            print help
        else:
            management.args.invalid_command_message(management.commands, exit_on_error=True)
    else:
        print "codenode-admin help:\n"
        print "\n".join(management.args.available_help(management.commands))

