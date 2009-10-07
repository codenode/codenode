######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

"""
Base runtime functions and classes for use in starting up python based
processes (i.e. python, sage...)

---------------------------------------------------------------
The Jail class and chroot testing were copied and modified from
 jailtools-0.1.py
 Copyright (C) 2006, 2007 Paul Boddie <paul@boddie.org.uk>
---------------------------------------------------------------

"""

import os

def build_env(config):
    """PYTHONPATH is usefull when codenode is not installed in the system
    """
    #env = {'PYTHONPATH':os.getenv('PYTHONPATH'),
    #        'HOME':os.getenv('HOME')}
    env = {}
    if os.environ.has_key('PYTHONPATH'):
        env['PYTHONPATH'] = os.getenv('PYTHONPATH') 
    if os.environ.has_key('HOME'):
        env['HOME'] = os.getenv('HOME') 
    if os.environ.has_key('PATH'):
        env['PATH'] = os.getenv('PATH') 
    return env

def build_jailed_env(config):
    """Set up environment variables to be used by engines of a uid != to
    the kernel server, in a chroot jail.
    """
    env = {}
    #Should this be relative to absolute root, or chroot?
    env['PYTHONPATH'] = config['engines-pythonpath']
    #HOME might be the same as the chroot
    env['HOME'] = config['engines-root']
    return env

def build_namespace():
    from codenode.backend.kernel.engine.python.introspection import introspect
    try:
        USERNAMESPACE = locals()
        USERNAMESPACE.update({"introspect":introspect})
    except ImportError:
        USERNAMESPACE={"introspect":introspect}
    return USERNAMESPACE



class ProcessSetup(object):

    def __init__(self, config, id, engines_uid, engines_gid=None):
        self.config = config
        self.id = id
        self.run_path = os.path.join(config['engines-path'], id)
        self.root = config['engines-root']
        self.engines_uid = engines_uid
        self.engines_gid = engines_gid
        #if engines_uid is None or int(config['engines-max']) > 1:
        #    self.change_user = True
        #else:
        #    self.change_user = False
        self.change_user = False

    def executable(self):
        raise "Specific Engines Must Implement this Method"

    def args(self, port):
        """port is an argument determined right before startup, and so is
        passed in here
        """
        if self.change_user:
            pythonpath = self.config['engines-pythonpath']
            start_script = self.jailed_engine_startup(port, 
                                                self.root,
                                                pythonpath, 
                                                self.engines_uid,
                                                self.engines_gid)
        else:
            start_script = self.engine_startup(port)
        a = (self.executable(), '-c', start_script, ) 
        return a

    def env(self):
        if self.change_user:
            return build_jailed_env(self.config)
        else:
            return build_env(self.config)

    def path(self):
        return self.run_path

    def uid(self):
        """
        Might not need this if engine processes setsuid itself
        engine_uid = self.config['engines-uid']
        if engine_uid == 'None':
            return None
        else:
            engine_uid = int(engine_uid)
        return engine_uid
        """
        return None

    def write_startup_file(self):
        """
        now only writes dir for notebook to run...
        """
        if not os.path.exists(self.run_path):
            os.mkdir(self.run_path)
        if self.change_user:
            os.chown(self.run_path, int(self.engines_uid), int(self.engines_gid))
            os.chmod(self.run_path, 0600) 

    def engine_startup(self, port):
        ENGINE_STARTUP="""
import sys
from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.python.interpreter import Interpreter
from codenode.backend.kernel.engine.python.runtime import build_namespace
namespace = build_namespace
server = EngineRPCServer(('127.0.0.1', %s), Interpreter, namespace)
server.serve_forever()
    """ % port
        return ENGINE_STARTUP

    def jailed_engine_startup(self, port, root, pythonpath, uid, gid):
        ENGINE_STARTUP="""
import sys
from codenode.backend.kernel.engine import base
from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.python.interpreter import Interpreter
from codenode.backend.kernel.engine.python.runtime import build_namespace
jail = base.Jail('%s', '%s', %s, %s)
entered = jail.enter_jail()
if not entered:
    sys.exit(1)
namespace = build_namespace
server = EngineRPCServer(('127.0.0.1', %s), Interpreter, namespace)
server.serve_forever()
        """ % (root, pythonpath, uid, gid, port, )
        return ENGINE_STARTUP








class Jail(object):
    """Addapted from jailtools-0.1.py by Paul Boddie <paul@boddie.org.uk>

    """

    def __init__(self, directory, pythonpath, uid, gid=None):
        self.directory = directory
        self.pythonpath = pythonpath
        self.uid = uid
        if gid is None:
            gid = uid
        self.gid = gid


    def enter_jail(self, test_breakouts=1):

        """
        Enter the jail using the details specified in the object's creation.

        If the optional 'test_breakouts' is set to a false value, a test of the
        jail will not be performed. Otherwise, the default behaviour is to test
        the jail by attempting to break out using a well-known technique for
        doing so, and to signal a compromise of the jail through a false return
        value (see below). Due to the behaviour of this technique when performed
        as the root user, the test must be suppressed if 'uid' is zero and
        'permit_root' is set in the creation of the jail object.

        Return whether the jail was successfully entered. If a false value is
        returned, it may be appropriate to abandon any subsequent operations and
        to exit the program immediately in order to prevent illegal access to
        resources outside the jail at potentially escalated privileges.
        """

        # Prevent breakouts if requested.
        paranoid = 0

        if test_breakouts:
            plans = plan_breakout(self.directory)
        # need to chdir?
        #os.chdir(self.directory)
        os.chroot(self.directory)
        os.setgid(self.gid)
        os.setuid(self.uid)
        env = {'PYTHONPATH':self.pythonpath}
        os.environ.update(env)

        # Test planned breakouts.

        if test_breakouts:
            return breakout_prevented(self.directory, plans, paranoid)

        return True

    def set_memory_limit(self, multiple):

        """
        Set the memory limit for the process according to the given 'multiple',
        where 1 represents the current memory usage, 2 represents twice the
        current memory usage, and so on. Floating point numbers for 'multiple'
        are permitted, but must be greater than one.
        """

        if multiple <= 1:
            raise ValueError, "The memory limit multiple must be greater than one."
        size_kilobytes = int(commands.getoutput("ps -p %d -o rss=" % os.getpid()))
        new_size_bytes = int(multiple * size_kilobytes * 1024)
        resource.setrlimit(resource.RLIMIT_AS, (new_size_bytes, new_size_bytes))

    def set_cpu_limit(self, t):

        """
        Set the CPU time limit to 't', where 't' is a length of time in seconds
        indicating the amount of time allowed for the process (in addition to
        the amount already used).
        """

        usage = resource.getrusage(resource.RUSAGE_SELF)
        cpu_used = usage[0] + usage[1]
        cpu_limit = int(cpu_used + t)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

    def set_file_limit(self, nfiles):

        "Set the limit on the number of open files to 'nfiles'."

        resource.setrlimit(resource.RLIMIT_NOFILE, (nfiles, nfiles))

    def set_file_size_limit(self, size):

        "Set the size limit on created files to 'size' bytes."

        resource.setrlimit(resource.RLIMIT_FSIZE, (size, size))

    def set_process_limit(self, nprocesses):

        """
        Set the limit on the number of new processes available to the jail's uid to
        'nprocesses'. This attempts to find out how many processes are already
        available to the user and then adds 'nprocesses' to the figure.
        """

        current_nprocesses = len(commands.getoutput("ps -u %s -o uid=" % self.uid).split("\n"))
        new_nprocesses = current_nprocesses + nprocesses + 1 # include the initial process
        resource.setrlimit(resource.RLIMIT_NPROC, (new_nprocesses, new_nprocesses))

def plan_breakout(directory):

    "Plan a breakout from the jail using the given 'directory'."

    parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
    filenames = os.listdir(parent_directory)
    filenames.sort()
    return parent_directory, filenames

def breakout_prevented(directory, plans, paranoid=0, breakout_directory="__tunnel__"):

    """
    Attempt a breakout from 'directory' using the given 'plans' supplied by a
    call to the 'plan_breakout' function. Return whether the breakout was
    prevented, employing additional tests if the optional 'paranoid' parameter
    is set to a true value. The attempt makes use of the widely publicised
    method, employing a temporary directory whose name can be specified
    explicitly using the optional 'breakout_directory' parameter.
    """

    outside_cwd, outside_filenames = plans
    cd = None

    # Perform the technique.

    try:
        # Required step: make a directory.

        if not os.path.exists(breakout_directory):
            os.mkdir(breakout_directory)

        # Optional step: open the current directory.

        try:
            cd = os.open(os.curdir, os.O_RDONLY)
        except OSError:
            pass

        # Required step: enter the directory.

        os.chroot(breakout_directory)

        # Optional step: open the current directory.

        if cd is not None:
            os.fchdir(cd)

    # Ignore permissions issues and keep testing.

    except OSError:
        pass

    # Tidy up.

    if cd is not None:
        os.close(cd)

    try:
        if os.path.exists(breakout_directory):
            os.rmdir(breakout_directory)
    except OSError:
        pass

    # Return success if the current working directory is the chroot location.

    if os.getcwd() == directory:
        return Status("False: cwd changed")

    # Otherwise, attempt to ascend the directory hierarchy.

    for n in range(0, 2):
        os.chdir(os.pardir)

        # View the filesystem.

        new_filenames = os.listdir(os.curdir)
        new_filenames.sort()
        new_cwd = os.getcwd()

        # Determine whether the filesystem appears to be from outside the jail.

        if outside_cwd == new_cwd:
            return Status("False: cwd outside")
        if paranoid and outside_filenames == new_filenames:
            return Status("False: filenames outside")

    return True

