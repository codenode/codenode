======
Knoboo
======
A new knoboo that:
    - Uses Django
    - Uses twisted.web
    - Is a current *Work in Progress, and is still broken/incomplete in several (fixable) places*


How to run knoboo
==================

Assuming you are in the top level 'knoboo' directory.

1) To run you *must* be using the Twisted trunk:
 svn co svn://svn.twistedmatrix.com/svn/Twisted/trunk Twisted

2) Initialize the database
 python knoboo/manage.py syncdb 
(say 'yes' to creating a superuser)

3) Start knoboo by running:
 Twisted/bin/twistd -n knoboo

4) Open up http://localhost:8000 and login with the 
   superuser account that was created from step 2.



============================
Development and code layout
============================

Kernel
========
Engines
-------
- The directory $knoboo/data is where each engines runtime enviroment exists.

- The file $knoboo/kernel/engine/base.py is where an 'engine' (actual process that
a notebook's code is executed in) specific config options (run_path, uid, guid, chroot jail, etc)

