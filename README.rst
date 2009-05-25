======
Knoboo
======
A new knoboo that:
    - Uses Django
    - Uses twisted.web
    - Is a current *Work in Progress, and is still broken/incomplete in several (fixable) places*


Dependencies
============
* Django  
* Twisted trunk
* knoboo 'master' branch


How to run knoboo
==================

IMPORTANT: Please follow these instructions *exactly*
-----------------------------------------------------
(This is because knoboo currently depends on a certain top-level 
directory structure, namely the Twisted trunk be called `Twisted`, to work,
this will change after the next release of Twisted.) 

**0. Make a new directory that both knoboo and Twisted will be downloaded to:**

::

  mkdir knobooenv
  cd knobooenv

**1. Download local dependencies:**

::

  svn co svn://svn.twistedmatrix.com/svn/Twisted/trunk Twisted
  git clone git://github.com/knoboo/knoboo.git

**2. Initialize the database (say 'yes' to creating a superuser):**

::

  cd knoboo
  python knoboo/manage.py syncdb 

**3. Start knoboo by running (Note the dependence of the Twisted trunk being one dir up):**

::

  ../Twisted/bin/twistd -n knoboo

**4. Open Firefox to http://APP_HOST:APP_PORT and login with the superuser account that was created from step 2.**



============================
Development and code layout
============================

Kernel
========

Engines
-------

- The directory 'data' is where each engines runtime environment exists.

- The file $knoboo/kernel/engine/base.py is where an 'engine' (actual process that
  a notebook's code is executed in) specific config options (run_path, uid, guid, chroot jail, etc)

