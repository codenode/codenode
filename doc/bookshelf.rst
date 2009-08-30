The Bookshelf
=============

The `Bookshelf` is one of the two central parts of codenode, (the other being a `Notebook`).  
The `Bookshelf` is the management interface to all `Notebooks` associated with a given user.
By drag-and-drop, or many checkbox selects, you can: add, delete, or archive `Notebooks`.  
Click the `Notebook` listing titles to sort and reverse-sort your `Notebooks`.
Create folders for storing related `Notebooks`.

[WORK IN PROGRESS]: From the `Bookshelf` you can search your `Notebooks`.  
Using the *Attach* button, you can upload static data to be associated 
with a given set of notebooks.  It is also possible to download `Notebooks` 
in portable, standalone formats, as well as upload standalone Knoboo notebooks, 
or Sage notebooks.


Add and Deleting Notebooks
--------------------------

^ Operation:
* *drag n drop* or click notebook radio button, then click action button.  TODO: give examples of this.
* `New Notebook` TODO:add kernel type options
* Move to trash, does not delete.  Need to empty Trash.
* Archive, save for later, but not likely used currently.

Sorting and Viewing
-------------------

* Title of each notebooks list column is clickable
  to perform a sorting action.  Clicking again performs
  the same sort, but in reverse.

Folders
-------

* Store related notebooks
* Changing title of folders
* How are folders displayed, ordering?


Search
------

* All the content of the notebooks are continually being
  indexed so as to provide searching capabilities of
  both the code and the text.

Attach
------

* TODO: this functionality needs to be robustified.

* Attach data to notebooks.
  Example: Upload a large file to perform parsing operations

* Provide the ability to supply a URL on the internet,
  and codenode will try to download the file and associate it
  with one or more notebooks.
