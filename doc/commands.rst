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


The "Frontend" twistd plugin is ``codenoded``.  For options type::

    $ twistd codenoded --help


The "Backend"  twistd plugin is ``codenode-kernel``.  For options type::

    $ twistd codenode-kernel --help






