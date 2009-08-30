The Notebook interface
=======================

Top bar buttons and features
----------------------------

* Save: save the state of the notebook
* Save and Close: save and close the notebook window, probably go back to
  the bookshelf
* Interrupt: interrupt/abort the current computation. Useful for canceling
  long running computations, infinite loops, etc. Aborts all pending
  evaluation requests as well. Does not affect the kernel session
  (namespace, computation results)
* Kill: completely stop the kernel. Lose namespace, objects/results in memory.
* Notebook title: change the notebook title by clicking on the name and typing an new one.


Cells
-----

* cell parts
      * left label/indicators
      * center, main input/content area
      * right, bracket indicating the context of the cell with respect to other
        cells (grouping/sectioning)
* evaluate
* output types 
    * textual
    * plot (image)
    * errors


Creating a new cell
-------------------
* Start a new cell by highlighting a 'spawn area' at the bottom of any cell


Evaluating code
---------------
Pressing the shift-enter key combination causes the code in an input cell
to be sent to the kernel for evaluation. The bracket will highlight to
indicate evaluation is in progress.
The results, if any, are displayed in an output cell created directly below
the input and an input number will appear to the left of the cell.


Sections and Grouping
---------------------

Cells can be organized into sections contained by a group cell.

Setting a cell as a heading type causes all the cells of lower section
level below it to be grouped into that section


Setting Cell Type
-----------------

To change a cells type, right click on the cell or the cell bracket and
select the type from the context menu.

Cell types:
* Section headings (non-evaluable):
    * Title: Highest level heading cell 
    * Subtitle
    * Section
    * SubSection: Lowest level heading cell
    * Input: (Default) Write code here
    * Output: Evaluation results 
    * Text: None evaluable text

Brackets
--------
Select a bracket by clicking on it. 
Delete cells by selecting a bracket and hitting the delete key.
Opening and closing groups: Double click on a group bracket.  
