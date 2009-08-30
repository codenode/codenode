QuickStart
==========

Usage
-----

^ Basic `codenode` usage, in 3 easy steps
#. Create a *New Notebook* (from the *New Notebook* dropdown menu). 
#. *Type 2+2* (Hover at top of blank white area, click when solid black line appears).
#. MOST IMPORTANT: **Hold down Shift and hit Enter** (to run the code).

^ More details of the above 3-step usage:
* When `codenode` first loads, you see the `Bookshelf`.  This is where you manage your `Notebooks`. 
* At the top left of the `Bookshelf`, click *New Notebook* to get started.
* After the `Notebook` loads, click on the top of the *blank white area* and a *solid black line* will appear.
* Now immediately type *2+2*, this creates your first `Cell`.  
* While holding down the *Shift Key*, hit *Enter* to run the code. *4* will appear below.
* You did it. Now create more `Cells`, or go back and change the one just created.


Install
-------

^Fast install. 
The quickest way to install in to use `easy_install`::

    $ easy_install codenode

^Recommended install.  
A better way to install `codenode` is to use pip+virtualenv::

    $ virtualenv --no-site-packages mycodenode_env
    $ pip -E mycodenode_env install codenode

With `virtualenv` you can create isolated Python environments, 
and then using pip you can directly install new packages into your `virtualenv`s.
Once you are through using a given `virtualenv`, it is safe to completely remove
it, and because it is self-contained, no traces of packages install will be left on
the system.  Using `virtualenv` is an excellent way to avoid Python package dependancy issues.
(you can download `virtualenv` via `easy_install virtualenv` or `pip install virtualenv`)


^Advanced install.
To try out the latest features in the master repository::

    $ virtualenv --no-site-packages codenode_env
    $ pip -E codenode_env install -e git://github.com/codenode/codenode.git#egg=codenode

To clone a copy for development::

    $ git clone git://github.com/codenode/codenode.git

