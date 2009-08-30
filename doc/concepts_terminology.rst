Important Concepts and Terminology
==================================

`codenode` has two central parts, the *Bookshelf* and the *Notebook*.

The `Bookshelf`
---------------
The `Bookshelf` is the management interface to all `Notebooks` and related data.

You can create folders for storing related `Notebooks`.
By drag-and-drop, or many checkbox selects, you can: add, delete, or archive `Notebooks`.
Click the `Notebook` listing titles to sort and reverse-sort your `Notebooks`.
From the `Bookshelf` you can also search your `Notebooks`.  


[WORK IN PROGRESS]: Using the *Attach* button, you can upload 
static data to be associated with a given set of notebooks.  
It is also possible to download `Notebooks` in portable, standalone formats, 
as well as upload standalone `codenode` notebooks, or Sage notebooks.


The `Notebook`
--------------
The `Notebook` is where you write and run code. 

A `Notebook` contains *code cells* and *text cells*.
Code cells are blocks of language specifc code for a given
language specific notebook (such as a Python Notebook).  Absolutely 
any code valid in a given language (such as Python) is valid in `codenode`. 

By **right-clicking** on a cell you can turn a cell into a text cell.
Text cells can either be section markers, such as title or subtitle
sections, or plain text that acts as documentation or context.



Glossary
--------

Attach:
    Associate static data (text, images) to one or more `Notebooks`, from inside the `Bookshelf`,
    allowing you to use this static data during a `Notebook` session.

Bookshelf:
    Where you manage all the notebooks you create.  You can start new Noteboo

Bracket:
    The blue bars on the far right-hand side of each 'Cell'.  Brackets indicate 
    'Cell' grouping.  *Double-click* on these brackets to open and close `Sections`. 

Cell:
    A textarea where you write code to be run (a 'code cell') or 
    you write text for documentation or context (a 'text cell').

Interrupt:
    Stop all currently executing cells.

Kill:
    Completely destroy the current notebook session. All variables and other state will be cleared.

Notebook:
    A self contained grouping of 'code cells' and 'text cells' that while active respects
    and unique process (Python, Sage, etc).  Defined variables, functions, etc are *not*
    shared between separate notebooks. 

Section:
    A logical grouping of many 'code cells' and 'text cells'.  Sections typically include a title,
    and/or subtitles, and several 'code cells'.  Sections can be collasped and expand by double-clicking
    the 'cell brackets' on the right.

