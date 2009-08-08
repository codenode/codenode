===============================================================
Codenode - Interactive Programming Notebook for the Web Browser
===============================================================

Quickstart
==========

**Quick Install:**

:: 

  $ easy_install codenode

::

  #Platform specific details:

  OSX (Must have Django >= 1.0 and Twisted >= 8.2):
  $ easy_install -U twisted django codenode

  Ubuntu / Debian:
  $ apt-get install python-django python-twisted python-setuptools python-dev build-essential
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
=======

Please ask any questions or give any feedback!
For help and feedback, go here: http://groups.google.com/group/codenode-devel
