The Kernel Server
=================

The *Kernel* and all associated *Engines* are the components
of `codenode` that handle the execution of a give Notebook's code.
The following is a techinical overview of the *Kernel* and all *Engines*
which combined is refered to as the "Backend" `codenode`.



Definitions
-----------

^Kernel (aka Kernel Server)
A Twisted application running these services:
#. Perspective-Broker server
#. Process Manager for managing computation engines

^Engine (aka. Computation Engine)
One process (Python, Sage, etc) where one notebooks computation takes place. 
Engines have two main parts:
#. XML-RPC server which provides a specific set of methods (according
    to the Engine interface/API) for the Kernel to call.
#. An Interpreter object with the same set of methods. The RPC server
    essentially wraps this interpreter giving it a network interface.

^Interpreter Object 
An object (implemented in a interpreted like Python), that provides 
a consistent interface (an API) to the fundamental capabilities 
of that language.
   

Overview
--------

The Kernel serves two purposes: 
#. Provides a network interface to the `codenode` application server for
relaying computation requests and results (data, plot images, etc.). 
#> Manages (starts, and stops) Engine processes.

**For every notebook running in a browser, there is one engine.**

The primary purpose of the *Interpreter Object* is to minimize the 
amount of specialized code that has to be added to it when a complex 
feature (like plotting or Mathematica like graphical interact). 

The most common operation a given language's interpreter can do
* execute code in a namespace
* store namespaces
* create and delete objects of specific types
* operate/introspect on object attributes/data



Implementation Details
----------------------

Before the Kernel Server can start up, it needs to know a few things:
* The port the Perspective broker server should listen on
* The env_path, which defaults to .knoboo/kernel. 

This is where it reads the conf and tac configuration files. 
* The conf file holds configuration parameters about what
  systems/programs are available (i.e. Python or Sage), what path the
  engines should run in, what uid the engine process should run as, and
  server parameters (host, and port) that will be used by twistd
  application.
* The tac is a config file that holds the twisted application 
  configuration script...it should really never need to be touched and
  is kind of a formalism until twisted application is more customized
  for codenode. 

The startup sequence 
(**FIXME**)
./kernel-start invokes /bin/codenode-kernel

... reads the command line options and parses through them for ones relevant to twistd
The twistd options include 
* daemonize?
* log file name/path
* pid file name/path
* location of tac file (this has to happen until the twisted Application
   is customized such that it doesn't need to read app config info from a
   tac file)

Then twistd application framework takes over...
It loads the tac file which reads the command line options again.
Now they are parsed for codenode application specifics.

The parsed options are stored in a dict which is passed to a function in
knoboo.main.py that puts together the services for the twisted application
object (this object is what the application framework is looking for)

For the kernel, the two services are 
* perspective broker server
* process manager

The main thing perspective broker does is invoke a Portal that holds the
Kernel Realm. The kernel Realm is very simple at this stage of development.

When a notebook is started in the application server, it connects to the
kernel server using the login method of the perspective broker
clientFactory. The pb realm authenticates using a hack credential/checker
that uses the same cleartext password for any avatarId (which are the
notebook Id's). Once login succeeds, the realm instantiates an
avatar/perspective for one engine. A reference to this is returned to the
app-server pb-client. The connection is now open and symmetric, therefore
the client never has to login (re-authenticate) again (the avatar persists
in memory with-out the realm storing an explicit public reference). This is
in stark contrast to the sessions managment that happens in guard.py, where
the inability of the HTTP protocol to maintain open symmetric connections
necessitates re-connection and re-authentication for every request and for
the avatar to be explicitly stored in a Sessions dictionary in the portal.
