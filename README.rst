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

  $ codenode-admin init -name mycodenode
  $ cd mycodenode
  $ codenode-admin run 
  #Now open browser to http://localhost:8000


**Running tests:**

  $ python setup.py nosetests 
  # See http://somethingaboutorange.com/mrl/projects/nose/ for full command line options, but 
  useful ones include --stop, --nocapture, --failed

Support
-------
Please ask any questions or give any feedback!
For help and feedback, go here: http://groups.google.com/group/codenode-devel


License
-------
Codenode is free software, licensed under the BSD. See the ``LICENSE`` file.
