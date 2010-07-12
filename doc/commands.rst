Commands For Running and Managing Codenode
==========================================

The codenode Command Line Admin Tool
------------------------------------
``codenode-admin`` is the tool to create, run, and manage codenode.

**Running codenode, quickstart**::

    $ codenode-admin init -desktop
    $ codenode-admin run -desktop
    #Now open browser to http://localhost:8000

For all options, run::

    $ codenode-admin --help


``codenode-admin``  exists as a tool to quickly get started,
and to easily run common commands.


Codenode environments
^^^^^^^^^^^^^^^^^^^^^

``codenode-admin`` needs to know where the environment for Codenode is.  It has several modes of
operation:

1. Running inside a directory created by ``codenode-admin init``.  This is the default mode.


2. Desktop mode.  This defaults to the directory ``~/.codenode`` and is intended for and end user.
You can activate this mode with the ``-desktop`` switch. 


3. Development mode.  This defaults an ``env`` directory inside the top of the source tree.  It 
also activates manholes for the frontend and backend.   Activate with the ``-devel`` switch.


4. Django and custom settings mode.  You can use Codenode as a Django installed app.  In this case, use the ``-settings mysite.settings`` switch, or set the 'DJANGO_SETTINGS_MODULE' environment variable.


In fact, ``codenode-admin`` largely are wrapper around the
following two command line tools of **Django** and **Twisted**.

For more advanced usage of `codenode`, it is very useful to
understand the capabilities of each tool.

To run `codenode` as a 'desktop application' (localhost only), use the
``run`` command. ``run`` starts the *frontend* and a local *backend*
automatically::

    $ codenode-admin run 

In a public deployment, the *frontend* and *backend* are run separately::

    $ codenode-admin frontend

and, similarly, on another server::

    $ codenode-admin backend

Killing the *backend* process will kill all child of its *engine*
processes.


django-admin.py
^^^^^^^^^^^^^^^

For more info, type::

    $ django-admin.py --help

[TODO] Describe usage (i.e. ``django-admin.py syncdb``),  and how it is wrapped.


twistd
^^^^^^

codenode includes three ``twistd`` Twisted command-line tool plugs.

For locally running codenode ("Fronted" and "Backend" combined),
the ``codenode`` ``twistd`` plugin in used, to see all options, type::

    $ twistd codenode --help


The "Frontend" twistd plugin is ``codenode-frontend``.  For options type::

    $ twistd codenode-frontend --help


The "Backend"  twistd plugin is ``codenode-backend``.  For options type::

    $ twistd codenode-backend --help





Development Command Tools
-------------------------

Use the ``-devel`` switch to activate the development settings.

- ``codenode-admin frontend -devel``
- ``codnode-admin backend -devel``
- ``codenode-admin frontendmanhole``
- ``codenode-admin backend-manhole``
- ``codenode-admin shell -devel``
- ``codenode-admin dbshell -devel``
- ``codenode-admin resetdb -devel``

See the section on :ref:`Development <development>`.


