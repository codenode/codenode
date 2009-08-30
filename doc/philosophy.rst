Motivation and philosophy of codenode
=====================================

Core ideas, user focused
------------------------

Getting things done in your web browser is really convenient.
Even better, it doesn't even have to be *your* web browser.
You can use the one at school, work, or your friends laptop to
send that important email or update your groups wiki page.

`codenode` creates an entire programming enviroment, in a web browser,
so you can run your code anywhere, at anytime.

Take for example a common situation:  You are at school or work,
and the computer you are on doesn't have a certain program installed,
it's a major hassle to install it yet again, assuming you have
permission to do so, or it ends up installing correctly.

With `codenode`, your code, data, and extra programs are stored and 
running somewhere else that you can rely on, just like your email.
You simply login to you account and get coding right away.

    
^Notebook
* Functionality (cells, evaluating, code goes to server is run and saved, result is displayed below)
* Usage (input, output, delete, sections).
* Interactive (experiment and refactor)
* Plotting.
* Tab-completion
* ? help.
* Save as source, text, pdf, html

^Bookshelf
* Organization.
* Management
* Sharing/Publishing
* Collaboration
* Upload/Download files
* Notebooks
* Modules
* Data



Core ideas, developer focused
-----------------------------

`codenode` is about creating a system that allows remote computation of
arbitrary code pieces, along with management of this
remote running code (like stopping evaluation, restarting)
and have the result of this computations be presented,
in a web browser, in a clean, modern, and useful way.

^What is a Kernel?
* The 'computation engine'
* The running process that evalautes code and keeps state (i.e. a persistent namespace to run code inside)
* The Kernel another machine (remote) or on the users machine (localhost)
* Decoupled backend (computation) and front-end (display)

^Kernel Connections
* Remote Perspective Broker
* Pexpect (cant use Pexpect on Windows)

^Security
* Django
* Sessions
* twisted.cred

^Data Management
* Django's Object Relational Mappers (ORM)
* Static Notebook resources (data files)

^Front End - Javscript / CSS
* jquery
* ajax
* comet

^Components: Django
* Views
* Templates
* Sessions
* Plugins

^Components: Twisted 
* A main "App Server", that controls high level access with "twisted.cred"
* Web frontend: "twisted.web"
* "Kernels":  lightweight XMLRPC servers, local namespace is the "computation enviroment"
* "Kernel Connections":  "twisted.pb" Perspective Broker
* "Kernel Managers":  start,stop, send signals with "twisted.internet.protocol.ProcessProtocol"
