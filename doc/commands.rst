Commands For Running and Managing Codenode
==========================================

The codenode Command Line Admin Tool
------------------------------------
``codenode-admin`` is the tool to create, run, and manage codenode.

**Running codenode, quickstart**::

    $ codenode-admin init -name mycodenode
    $ cd mycodenode
    $ codenode-admin run
    #Now open browser to http://localhost:8000


For all options, run::

    $ codenode-admin --help


``codenode-admin``  exists as a tool to quickly get started,
and to easily run common commands.

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

- ``make-devel-env``
- ``frontend-devel``
- ``backend-devel``
- ``frontend-manhole``
- ``backend-manhole``
- ``frontend-models-shell``


See the section on :ref:`Development <development>`.


