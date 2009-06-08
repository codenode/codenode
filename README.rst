===============================================================
Codenode - Interactive Programming Notebook for the Web Browser
===============================================================

Quickstart
==========

**1. Install Dependencies:**

:: 

  #Requires Twisted 8.2.0 and Django 1.0

  OSX: 
  $ easy_install -U twisted django
  
  Ubuntu / Debian:
  $ apt-get install python-django python-twisted

  (Recommended: Use "virtualenv")

**2. Download and Install Codenode:**

::

  $ wget http://cloud.github.com/downloads/codenode/codenode/codenode-v0.01.tar.gz
  $ tar zxvf codenode-v0.01.tar.gz
  $ cd codenode-v0.01; python setup.py install; cd ..

**3. Start a codenode:**

::

  $ codenode-admin init -name mycodenode
  $ cd mycodenode
  $ codenode-admin run 

**4. Open Firefox and login:**

::

  1. Go to localhost:8000
  2. Log in as user "admin" and password "admin"
  3. Create and New Notenook and go.
