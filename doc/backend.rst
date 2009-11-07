The Backend
===========

.. _backend:


The *Backend* is a container for managing notebook *engine*
processes. Every notebook running in a web browser corresponds to one
*backend* *engine* process. 

The *Backend* starts *engine* processes and provides a mechanism for
interacting with the *engine* interpreter when it is running. *Engine*
types are registered with the *backend* through plug-in files. Plug-in
files can be added or subtracted at any time the server is running. 

A *Frontend* server is associated with one or more *backends*, each of
which may be running anywhere on the network, including the localhost.

The *backend* is set up so that the concerns of how code actually gets
executed is separate from how code is moved in and out of the web browser
and saved in the database. The *frontend* is responsible for managing the
database, and the code execution aspect of the system is handled by the *engine*. 

Backend Server
--------------

The *backend* provides a general API for managing and interfacing
*engines*. The *frontend* queries the *backend* through an administrative
channel for information on what *engine* types it provides, etc. and
allocates *engine* usage for the notebooks owned by its registered users. 

The *backend* does not know about notebooks or users registered in the
*frontend* -- the *backend* only knows about what *engines* it can run and
what *engines* are currently running. A *notebook* communicates to an
*engine* through a *frontend*-owned communication bus which, in turn,
talks to a *backend* where the *engine* lives.

Engine
------

*Engine* is the name for the process that actually runs the code entered in
the web browser. 

An *engine* is something that produces output given some input. The design
of *Codenode* does not make assumptions on precisely what an *engine* does
or how it does it, but in general, it provides a way to execute arbitrary
code. `Codenode` provides an implementation of one *engine*, the Python
interpreter engine. The Python engine executes the code users enter in the
notebook from the web browser. The Python engine is something that adapts
the general Python interpreter REPL (read-eval-print loop) into an abstract
thing callable from anywhere, like a service for computation.


The current implementation of the default Python *engine* is an object that
provides a way to execute arbitrary python code input as a string. The
object provides other second-order methods like 'complete', which
facilitates the notebooks tab-completer.::

    >>> from codenode.engine import interpreter
    >>> in1 = interpreter.Interpreter()
    >>> in1.evaluate('2+2')
    {'input_count': 1, 'out': '4\n', 'cmd_count': 1, 'err': '', 'in':
    '2+2'}
    >>> in1.evaluate('a = 12')
    {'input_count': 2, 'out': '', 'cmd_count': 1, 'err': '', 'in': 'a =
    12'}
    >>> in1.evaluate('a + a')
    {'input_count': 3, 'out': '24\n', 'cmd_count': 1, 'err': '', 'in': 'a +
    a'}

    >>> in2 = interpreter.Interpreter()
    >>> in2.evaluate('a + a')
    {'input_count': 1, 'out': '', 'cmd_count': 1, 'err': 'Traceback (most
    recent call last):\n  File "<input>", line 1, in <module>\nNameError:
    name \'a\' is not defined\n', 'in': 'a + a'}
    >>> in2.evaluate('a = 42')
    {'input_count': 2, 'out': '', 'cmd_count': 1, 'err': '', 'in': 'a =
    42'}
    >>> in2.evaluate('print a')
    {'input_count': 3, 'out': '42\n', 'cmd_count': 1, 'err': '', 'in':
    'print a'}
    >>> in1.evaluate('print a')
    {'input_count': 4, 'out': '12\n', 'cmd_count': 1, 'err': '', 'in':
    'print a'}
    >>> 


This separation of interpreter object and RPC server within the *engine*,
as well as the distinction between *backend server* and *engine process*,
creates a flexible and friendly development environment with a low barrier
of entry. New *engine* types can be developed by following a simple recipe,
adding non-trivial functionality without modifying the internals of
`codenode`.   

Engine Plug-in files
^^^^^^^^^^^^^^^^^^^^

A *backend* supports running one or more types of *engines*. 
*Engine* types are added to a *backend* via plug-in files. Plug-in files
live in the twisted/plugins directory of your `codenode` environment
directory.

An *engine* plug-in is a file written in the Python language. The plug-in
specifies the essential attributes of an operating system process (e.g. bin
path to invoke, command line arguments, environment variables, etc.). 

The `codenode` source tree includes an example of a non-trivial *engine
plug-in* for running *Sage*. 



