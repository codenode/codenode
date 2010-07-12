Developing Codenode
===================

.. _development:

The development scripts are for running codenode components straight
from the repository source tree. They facilitate a more convenient
development work flow as committable changes to the source can be tested
with no re-build or re-installing. 

Hackable Components
-------------------
Condenode is separated into a few systems each providing a distinct set of
functionality. 

- Browser client (JavaScript program, HTML structure, CSS style)
- Frontend server
- Backend server
- Computation engine

As an Open Source project, one important design goal is to make it so
non-trivial work on any given component does not require deep understanding
of the entire system. This provides contributors who may be particularly
good at something like, say, JavaScript, but who also may be unexperienced with
Twisted or Django, a minimally hindered development environment.


Dependencies should be available in your PYTHONPATH. It is recommended
that developers install all dependencies in a virtualenv when using the
devel scripts to run codenode components. 

Overview
^^^^^^^^
- Convenience scripts for running *Frontend* and *Backend* servers
- Convenience script for creating a codenode *environment* dir with
  o database synced with the latest models
  o latest default settings files for frontend and backend
  o latest twistd server plugin files
  o latest django template files
- models-shell script for playing with frontend django models in the ipython
  command line interpreter.
- Manhole scripts for dropping into the running frontend or backend server
  processes. 


Server scripts
--------------

``codenode-admin frontend -devel`` runs the frontend server of codenode. This uses library code
from codenode.service, codenode.frontend and relies on the
twisted/plugins/frontend_plugin.py file.

``codenode-admin backend -devel`` runs the backend server of codenode. This server uses
codenode.backend and codenode.engine and relies on the
twisted/pliguins/backend_plugin.py file.


Devel environment and database
------------------------------

The ``-devel`` switch to codenode-admin activates the development environment and if necessary
creates a dir called env in the codenode/devel dir. *env* is called a codenode *environment* and is the development version of::

    $ codenode-admin init -devel


``codenode-admin resetdb -devel`` can be used to reset the frontend database without recreating all of the env environment.


Devel mode example
------------------

Open up a terminal and type::

    $ codenode-admin frontend -devel

Open a second terminal and type::

    $ codenode-admin backend -devel

Now go to http://localhost:8000/admin, log in with the username and
password that you entered from ``./make-devel-env``, and go to
"Backend servers" and add a new, with "Server address" being "http://localhost:8337".


Manhole
-------

Manhole is a Twisted tool. Manhole allows you to telnet or ssh into
part of the namespace of a running Twisted server! Running either frontend
or backend version of this tool drops you into what looks like a python
command line interpreter, from which you have access to the object
instances setup in either codenode.service or codenode.backend.server. 
By invoking appropriate methods found in twisted.python.rebuild, you can
dynamically rebuild modules and classes without restarting the server! More
elaborate and convenient use cases can, and hopefully will, grow out of
this raw capability.

You can enter a manhole with ``codenode-admin frontendmanhole`` or ``codenode-admin backendmanhole``


Running Tests
-------------

To run tests, you must install `django-nose` and `nose`.

The call the suite, run `test.sh` from the top level directory.

