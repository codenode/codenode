Codenode - Interactive Programming Notebook for the Web Browser
===============================================================

For complete documentation, please see: http://codenode.org/docs

Quickstart
----------

**Quick Install:**

::

  $ easy_install codenode


**Recommend Install:**

:: 

  $ easy_install -U virtualenv pip 
  $ virtualenv --no-site-packages mycodenode_env
  $ pip -E mycodenode_env install codenode


**Quick Start:**

::

  $ codenode-admin codenode_desktop
  
Now open browser to http://localhost:8000


**Running tests:**

::

  $ run ./test.sh in this directory
  
Requires installation of nose and django_nose. See http://somethingaboutorange.com/mrl/projects/nose and http://github.com/jbalogh/django-nose

If you have pip installed, it can be as easy as: 

::
  
  $ pip install nose
  $ pip install django-nose
  

Support
-------
Please ask any questions or give any feedback!
For help and feedback, go here: http://groups.google.com/group/codenode-devel


License
-------
Codenode is free software, licensed under the BSD. See the ``LICENSE`` file.
