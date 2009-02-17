##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 

import os
import sys
import getpass
from string import Template
from ConfigParser import ConfigParser

from twisted.python import usage


_true_strings = ('true', 'on', '1')
_false_strings = ('false', 'no', '0')

def coerce_bool_option(string):
    string = str(string)
    if string.lower() in _true_strings:
        return 1
    if string.lower() in _false_strings:
        return 0
    return string


class UserProfile:
    """Check the file system for configuration.

       Application directories are created in
       '$HOME/.knoboo' if they do not exist.
    """

    def __init__(self, env_path='', db_driver="sqlite3"):
        joinpath = os.path.join
        home = env_path or os.getenv('HOME')
        self._dotkb_path = joinpath(home, '.knoboo')
        self._knoboo_path = joinpath(self._dotkb_path, 'knoboo')
        self._knoboo_conf_name = 'knoboo.conf'
        self._knoboo_conf_path = joinpath(self._knoboo_path, self._knoboo_conf_name)
        self._db_driver = db_driver
        self._db_main = 'knoboo.db'
        self._db_search = 'search.db'
        self._db_main_path = joinpath(self._knoboo_path, self._db_main)
        self._db_search_path = joinpath(self._knoboo_path, self._db_search)
        self._kernel_path = joinpath(self._dotkb_path, 'kernel')

    def new_userQ(self):
        return not os.path.exists(self._knoboo_path)

    def create_user_profile(self):
        """Main point of creation of user profile.

        If the profile already exists, do nothing.
        """
        self.dot_knoboo()
        self.make_knoboo()
        self.make_default_knoboo_tac()
        self.make_default_db()
        sr = self.make_default_knoboo_conf()
        return sr

    def dot_knoboo(self):
        if not os.path.exists(self._dotkb_path):
            os.mkdir(self._dotkb_path)

    def make_knoboo(self):
        kp = self._knoboo_path
        os.mkdir(kp)
        os.mkdir(os.path.join(kp, "data"))
        os.mkdir(os.path.join(kp, "images"))
        os.mkdir(os.path.join(kp, "prints"))

    def make_default_knoboo_conf(self):
        import knoboo
        path = knoboo.__path__[0]
        sage_root = self.ask_for_sage_path()
        conffile = open(self._knoboo_conf_path, 'w')
        d = {'db_main_path':self._db_main_path, 
            'db_search_path':self._db_search_path, 
            'db_driver':self._db_driver,
            'static_path':os.path.join(path, 'static'),
            'kernel_path':self._kernel_path}
        def_conf = Template(DEFAULT_USER_SERVER).substitute(d)
        conffile.writelines(def_conf)
        conffile.close()
        return sage_root

    def make_default_knoboo_tac(self):
        """hack for now...XXX
        """
        import knoboo
        path = knoboo.__path__[0]
        f = file(os.path.join(path,'knoboo.tac'), 'r')
        tac = f.read()
        f.close()
        f = file(os.path.join(self._knoboo_path, 'knoboo.tac'), 'w')
        f.write(tac)
        f.close()
        f = file(os.path.join(path,'knoboo_desktop.tac'), 'r')
        tac = f.read()
        f.close()
        f = file(os.path.join(self._knoboo_path, 'knoboo_desktop.tac'), 'w')
        f.write(tac)
        f.close()
        f = file(os.path.join(path,'printing', 'knoboo_notebook.sty'), 'r')
        sty = f.read()
        f.close()
        f = file(os.path.join(self._knoboo_path, 'prints', 'knoboo_notebook.sty'), 'w')
        f.write(sty)
        f.close()


    def make_default_db(self):
        pass
        
    def ask_for_sage_path(self):
        msg = "Enter your Sage installation full path or hit 'Enter'\n" 
        msg += "(can be changed later in '$HOME/.knoboo/kernel/kernel.conf'):"
        print msg
        sage_root = raw_input()
        return sage_root

class KernelProfile:
    """Kernel server profile
    """

    def __init__(self):
        joinpath = os.path.join
        home = os.getenv('HOME')
        self._dotkb_path = joinpath(home, '.knoboo')
        self._kernel_path = joinpath(self._dotkb_path, 'kernel')
        self._kernel_conf_name = 'kernel.conf'
        self._kernel_conf_path = joinpath(self._kernel_path, self._kernel_conf_name)
        self._kernel_env_path = joinpath(self._kernel_path, 'kernel_env')

    def new_kernelQ(self):
        return not os.path.exists(self._kernel_path)

    def create_kernel_profile(self, sage_root):
        self.dot_knoboo()
        self.make_kernel()
        self.make_default_kernel_server_conf(sage_root)
        self.make_kernel_env()
        self.make_default_kernel_tac()

    def dot_knoboo(self):
        if not os.path.exists(self._dotkb_path):
            os.mkdir(self._dotkb_path)

    def make_kernel(self):
        os.mkdir(self._kernel_path)

    def make_default_kernel_server_conf(self, sage_root):
        conffile = open(self._kernel_conf_path, 'w')
        d = {'sage_root':sage_root,
                'engines_path':os.path.join(self._kernel_path, 'kernel_env')}
        def_conf = Template(DEFAULT_KERNEL_SERVER).substitute(d)
        conffile.writelines(def_conf)
        conffile.close()

    def make_kernel_env(self):
        os.mkdir(self._kernel_env_path)

    def make_default_kernel_tac(self):
        """hack for now...XXX
        """
        import knoboo
        path = knoboo.__path__[0]
        f = file(os.path.join(path,'kernel.tac'), 'r')
        tac = f.read()
        f.close()
        f = file(os.path.join(self._kernel_path, 'kernel.tac'), 'w')
        f.write(tac)
        f.close()

def check_user():
    c = UserProfile()
    if c.new_userQ():
        sage_root = c.create_user_profile()
        check_kernel(sage_root)

def check_kernel(sage_root=None):
    c = KernelProfile()
    if c.new_kernelQ():
        c.create_kernel_profile(sage_root)


class DesktopOptions(usage.Options):
    """Main command line options for the desktop server.
     - host name
     - port number
     - proxy configuration
     - secure, use ssl

    """

    optParameters = [
            ['host', 'h', None],
            ['port', 'p', None, 'Port number to listen on'],
            ['kernel_host', 'k', None, 'kernel Server host'],
            ['kernel_port', 'q', None, 'Kernel Server port'],
            ['env_path', 'e', os.path.join(os.getenv('HOME'), '.knoboo', 'knoboo'), 
                'Path containing config, tac, and db'],
        ]

    optFlags = [
            ['secure', 's', 'Use HTTPS SSL'],
            ['devel_mode', 'd', 'Development mode'],
            ['nodaemon', 'n', "don't daemonize"],
            ['open_browser', 'b', 'Automatically open web browser']
        ]

    def __init__(self):
        usage.Options.__init__(self)
        usage.Options.parseOptions(self)

    def get_twistd_options(self):
        """returns flags and parameters for twistd.
        """
        topts = []
        env_path = self['env_path']
        if self['nodaemon']:
            topts.append('-n')
        else:
            topts.append('-l')
            log_path = os.path.join(env_path, 'knoboo_desktop.log')
            topts.append(log_path)
            topts.append('--pidfile')
            pid_file = os.path.join(env_path, 'knoboo_desktop.pid')
            topts.append(pid_file)
        tac_path = os.path.join(env_path, 'knoboo_desktop.tac')
        topts.append('-y')
        topts.append(tac_path)
        return topts

    def parseConfigFile(self):
        """Reads defaults for all parameters from configuration file
        contained in env_path. 

        With proper defaults set for all paramaters/flags, the command line
        options are re-parsed.

        set_config_dict adds convience sub-sections to self for use in the
        system.
        """
        env_path = self['env_path']
        self.dconfig = ConfigParser()
        config_filename = os.path.join(env_path, 'knoboo.conf')
        self.dconfig.read(config_filename)
        self.set_adhoc_defaults_from_conf()
        self.set_config_dict()

    def set_adhoc_defaults_from_conf(self):
        """overwrite default options 
        """
        defs = []
        secs = self.dconfig.sections()
        for sec in secs:
            defs.extend(self.dconfig.items(sec))
        defs = dict(defs)
        self.defaults.update(defs)
        self.update(defs)
        usage.Options.parseOptions(self)

    def set_config_dict(self):
        """Setup config object to be used within the system while it is
        running.
        Map divisions of subsections with in conf file to sub-dicts of the
        config object.
        """
        server = self.dconfig.items('server')
        self.server = {}
        for o, d in server:
            self.server[o] = coerce_bool_option(self[o])
        kernel = self.dconfig.items('kernel')
        self.kernel = {}
        for o, d in kernel:
            self.kernel[o] = self[o]
        db = self.dconfig.items('database')
        self.db = {}
        for o, d in db:
            self.db[o] = self[o]

    def postOptions(self):
        """Make sure the default env .knoboo is there
        If .knoboo does not exist:
         - could be new user, create .knoboo
        else:
         - user specified another path, check for it
        """
        if self.defaults['env_path'] == self['env_path']:
            check_user()
            return
        if not os.path.exists(self['env_path']):
            raise usage.UsageError, 'path to app environment does not exist!'

    def opt_version(self):
        print 'Knoboo Desktop version: 0.1'
        sys.exit(0)

class ServerOptions(usage.Options):
    """Main command line options for the app server.
     - host name
     - port number
     - proxy configuration
     - secure, use ssl

    """

    optParameters = [
            ['host', 'h', None],
            ['port', 'p', None, 'Port number to listen on'],
            ['kernel_host', 'k', None, 'kernel Server host'],
            ['kernel_port', 'q', None, 'Kernel Server port'],
            ['static_path', None, None, 'Static path for web server'],
            ['url_root', 'u', '/', 'Root url path for web server'],
            ['url_static_root', 's', '/', 'Static root url path for web server'],
            ['env_path', 'e', os.path.join(os.getenv('HOME'), '.knoboo', 'knoboo'), 
                'Path containing config, tac, and db'],
        ]

    optFlags = [
            ['secure', None, 'Use HTTPS SSL'],
            ['proxy', 'r', 'Use in reverse proxy configuration'],
            ['devel_mode', 'd', 'Development mode'],
            ['nodaemon', 'n', "don't daemonize"],
        ]

    def __init__(self):
        usage.Options.__init__(self)
        usage.Options.parseOptions(self)

    def get_twistd_options(self):
        """returns flags and parameters for twistd.
        """
        topts = []
        env_path = self['env_path']
        if self['nodaemon']:
            topts.append('-n')
        else:
            topts.append('-l')
            log_path = os.path.join(env_path, 'knoboo.log')
            topts.append(log_path)
            topts.append('--pidfile')
            pid_file = os.path.join(env_path, 'knoboo.pid')
            topts.append(pid_file)
        tac_path = os.path.join(env_path, 'knoboo.tac')
        topts.append('-y')
        topts.append(tac_path)
        return topts

    def parseConfigFile(self):
        """Reads defaults for all parameters from configuration file
        contained in env_path. 

        With proper defaults set for all paramaters/flags, the command line
        options are re-parsed.

        set_config_dict adds convience sub-sections to self for use in the
        system.
        """
        env_path = self['env_path']
        self.dconfig = ConfigParser()
        config_filename = os.path.join(env_path, 'knoboo.conf')
        self.dconfig.read(config_filename)
        self.set_adhoc_defaults_from_conf()
        self.set_config_dict()

    def set_adhoc_defaults_from_conf(self):
        """overwrite default options 
        """
        defs = []
        secs = self.dconfig.sections()
        for sec in secs:
            defs.extend(self.dconfig.items(sec))
        defs = dict(defs)
        self.defaults.update(defs)
        self.update(defs)
        usage.Options.parseOptions(self)

    def set_config_dict(self):
        """Setup config object to be used within the system while it is
        running.
        Map divisions of subsections with in conf file to sub-dicts of the
        config object.
        """
        server = self.dconfig.items('server')
        self.server = {}
        for o, d in server:
            self.server[o] = coerce_bool_option(self[o])
        kernel = self.dconfig.items('kernel')
        self.kernel = {}
        for o, d in kernel:
            self.kernel[o] = self[o]
        db = self.dconfig.items('database')
        self.db = {}
        for o, d in db:
            self.db[o] = self[o]

    def postOptions(self):
        """Make sure the default env .knoboo is there
        If .knoboo does not exist:
         - could be new user, create .knoboo
        else:
         - user specified another path, check for it
        """
        if self.defaults['env_path'] == self['env_path']:
            check_user()
            return
        if not os.path.exists(self['env_path']):
            raise usage.UsageError, 'path to app environment does not exist!'

    def opt_version(self):
        print 'Knoboo WebApp version: 0.1'
        sys.exit(0)

def easyServerOptions():
    config = ServerOptions()
    config.parseConfigFile()
    return config


class KernelServerOptions(usage.Options):
    """Options for the kernel server
    """

    optParameters = [
            ['host', 'h', 'localhost'],
            ['port', 'p', '8337', 'Port number to listen on'],
            ['env_path', 'e', os.path.join(os.getenv('HOME'), '.knoboo', 'kernel'), 
                'Path containing config, tac, and db'],
            ['engines-path', None, os.path.join(os.getenv('HOME'),
                '.knoboo', 'kernel', 'kernel_env'),
                'run-path for engine processes'],
            ['engines-root', None, None, 
                'root path for chroot of engine process'],
            ['engines-pythonpath', None, None, 'Packages in chroot jail'],
            ['engines-uid', 'u', None, 
                'uid of engine processes. Overriden if max-engines > 1'],
            ['engines-gid', 'g', None, 'gid of engine processes'],
            ['engines-max', 'm', 1, 
                'Maximum number of simultaneous engine processes'],
        ]

    optFlags = [
            ['secure', 's', 'Use HTTPS SSL'],
            ['proxy', 'r', 'Use in reverse proxy configuration'],
            ['nodaemon', 'n', "don't daemonize"]
        ] 

    def __init__(self):
        usage.Options.__init__(self)
        usage.Options.parseOptions(self)

    def get_twistd_options(self):
        topts = []
        self.parseOptions()
        env_path = self['env_path']
        if self['nodaemon']:
            topts.append('-n')
        else:
            topts.append('-l')
            log_path = os.path.join(env_path, 'kernel.log')
            topts.append(log_path)
        topts.append('--pidfile')
        pid_file = os.path.join(env_path, 'kernel.pid')
        topts.append(pid_file)
        tac_path = os.path.join(env_path, 'kernel.tac')
        topts.append('-y')
        topts.append(tac_path)
        return topts

    def parseConfigFile(self):
        env_path = self['env_path']
        self.dconfig = ConfigParser()
        config_filename = os.path.join(env_path, 'kernel.conf')
        self.dconfig.read(config_filename)
        self.set_adhoc_defaults_from_conf()
        self.set_config_dict()

    def set_adhoc_defaults_from_conf(self):
        """overwrite default options 
        """
        defs = []
        secs = self.dconfig.sections()
        for sec in secs:
            defs.extend(self.dconfig.items(sec))
        defs = dict(defs)
        self.defaults.update(defs)
        self.update(defs)
        usage.Options.parseOptions(self)

    def set_config_dict(self):
        """Setup config object to be used within the system while it is
        running.
        Map divisions of subsections with in conf file to sub-dicts of the
        config object.
        """
        server = self.dconfig.items('server')
        self.server = {}
        for o, d in server:
            self[o] = coerce_bool_option(self[o])
        self.systems = self.dconfig.options('systems')
        if self['engines-path'] == None:
            self['engines-path'] = os.path.join(self['env_path'], self.dconfig.get('kernel', 'engines-path')) 

    def setDefaultConfig(self):
        server = self.dconfig.items('server')
        for o, d in server:
            self[o] = coerce_bool_option(d)
 
    def postOptions(self):
        """Make sure the default env .knoboo is there
        """
        if self.defaults['env_path'] == self['env_path']:
            check_kernel()
            return
        if not os.path.exists(self['env_path']):
            raise usage.UsageError, 'path to app environment does not exist!'

    def opt_version(self):
        print 'Knoboo Kernel version: 0.1'
        sys.exit(0)


DEFAULT_USER_SERVER = """
[server]
host = localhost
port = 8000
static_path = 
secure = 0
proxy = 0
devel_mode = 0
url_root = /
url_static_root = /

[database]
driver = $db_driver
main_path = $db_main_path
search_path = $db_search_path

[kernel]
kernel_host = localhost
kernel_port = 8337
kernel_path = $kernel_path
"""



DEFAULT_APP_SERVER = """
[server]
secure = 0
host = localhost
port = 8000
proxy = 0
static_path = $static_path 
devel_mode = 0
url_root = /
url_static_root = /

[db]
driver = $db_driver
main_path = $db_main_path
search_path = $db_search_path

[kernel]
kernel_host = localhost
kernel_port = 8337
kernel_path = $kernel_path

"""

DEFAULT_KERNEL_SERVER = """
[server]
host = localhost
port = 8337
secure = 0
proxy = 0

#change to engines subgroup (instead of kernel)
[kernel]
#change to engines-run-path
engines-path = $engines_path
#change to engines-root-path OR engines-jail-root
engines-uid = None
engines-group = None
engines-max = 1
engines-user-prefix = nbu
engines-root = None
engines-pythonpath: %(engines-root)s/packages
engines-mem-limit = None
engines-cpu-limit = None
engines-file-limit = None
engines-file-size-limit = None
engines-process-limit = None



[systems]
python = 1
sage = 1

[python]
bin = python
full_bin = python

[sage]
bin = python
sage_root = $sage_root
full_bin: %(sage_root)s/local/bin/python
home = None

"""



