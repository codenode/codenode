.. _concepts_terminology:

Important Concepts and Terminology
==================================

.. _concepts:

`codenode` has two central parts, the **Bookshelf** and the **Notebook**.

The `Bookshelf`
---------------
The `Bookshelf` is the management interface to all `Notebooks` and related data.

Features:
    * Create folders for storing related `Notebooks`.
    * Add, Delete, or Archive `Notebooks` by drag-and-drop or checkboxes.
    * Sort `Notebooks` by clicking the topbar header of the `Notebook` listing.
    * Search the content of all `Notebooks`.  

.. seealso::
    For more `Bookshelf` details and screenshot, see :ref:`here <bookshelf>`.



The `Notebook`
--------------
The `Notebook` is where you write and run code. 

A `Notebook` contains *code cells* and *text cells*.
Code cells are blocks of language specific code for a given
language specific notebook (such as a Python Notebook).  Absolutely 
any code valid in a given language (such as Python) is valid in `codenode`. 

By **right-clicking** on a Cell, you can turn a Cell into a "Text Cell".
Text cells can either be section markers, such as title or subtitle
sections, or plain text that acts as documentation or context.


.. seealso::
    For more `Notebook` details and screenshot, see :ref:`here <notebook>`.


.. _glossary_of_terms:

Glossary of key terms in codenode
---------------------------------

**Attach**:
    [WORK IN PROGRESS] Associate static data (text, images) to one or more `Notebooks`, from inside the `Bookshelf`,
    allowing you to use this static data during a `Notebook` session.

**Backend**:
    The component of `**codenode**` where code execution occurs. 
    Designed to be run remotely or locally. See <the

**Bookshelf**:
    Where you manage all the notebooks you create.

**Bracket**:
    The blue bars on the far right-hand side of each 'Cell'.  Brackets indicate 
    'Cell' grouping.  `Double-click` on these brackets to open and close `Sections`. 

**Cell**:
    A textarea where you write code to be run (a 'Code Cell') or you write text 
    for documentation or context (a 'Text Cell').

**Interrupt**:
    Stop all currently executing cells.

**Kill**:
    Completely destroy the current notebook session. All variables and other state will be cleared.

**Notebook**:
    A self contained grouping of 'Code Cells' and 'Text Cells' that while active respects
    and unique process (Python, Sage, etc).  Defined variables, functions, etc are *not*
    shared between separate notebooks. 

**Section**:
    A logical grouping of many 'Code Cells' and 'Text Cells'.  Sections typically include a title,
    and/or subtitles, and several 'Code Cells'.  Sections can be collapsed and expand by double-clicking
    the 'Cell Brackets' on the right.

