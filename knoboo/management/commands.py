import os
import shutil
import knoboo
from knoboo import management

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
    os.mkdir(envroot)
    for dir in ["frontend", "backend"]:
        os.makedirs(osjoin(envroot, dir))

    pkgroot = os.sep.join(knoboo.__file__.split(os.sep)[:-1])

    frontendsettingsfile = osjoin(osjoin(pkgroot, "frontend"), "_settings.py")
    shutil.copyfile(frontendsettingsfile,  osjoin(osjoin(envroot, "frontend"), "settings.py"))
    open(osjoin(osjoin(envroot, "frontend"), "__init__.py"), "w").close()

    backendsettingsfile = osjoin(osjoin(pkgroot, "backend"), "_settings.py")
    shutil.copyfile(backendsettingsfile,  osjoin(osjoin(envroot, "backend"), "settings.py"))
    open(osjoin(osjoin(envroot, "backend"), "__init__.py"), "w").close()

    staticroot = osjoin("frontend", "static")
    pkgstaticroot = osjoin(pkgroot, staticroot)
    shutil.copytree(pkgstaticroot, osjoin(envroot, staticroot))

    compressroot = osjoin("frontend", "compress")
    pkgcompressroot = osjoin(pkgroot, compressroot)
    shutil.copytree(pkgcompressroot, osjoin(envroot, compressroot))

    pkgdataroot = osjoin(pkgroot, "data")
    shutil.copytree(pkgdataroot, osjoin(envroot, "data"))

    pkgtwistedroot = osjoin(pkgroot, "twisted")
    shutil.copytree(pkgtwistedroot, osjoin(envroot, "twisted"))


def run_command(daemonize=False): #, frontendpid=None, kernelpid=None):
    """
    Run a codenode.  Use inside a directory created with "codenode-admin init".

    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'
    abspath = os.path.abspath(".")
    os.system("twistd -n knoboo --env_path=%s" % abspath)


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

