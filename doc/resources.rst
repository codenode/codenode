Resources - Objects that Response to Request for Data or Actions
================================================================


Introduction
------------

Abstractly, `Resources` are objects that have logic to
handle `Requests` for some operation to occur.

In practice, with respect to Knoboo, a `Resource` is
an object that accepts a `Request` from a `Client`, and
performs an `Action` given HTTP `Header` information,
and HTTP POST and GET args.

This `Action` is typically one of the following:

    1) Request a state change ::

       "Delete the cell with id '123'" or 
       "Change the background color of notebook with id '987'"
        and the success or failure of this `Request` is 
        Responded back to the client as a simple "success/fail".

    2) Request data ::

        "Evaluate Cell with id "357" which has content "2+2"
        and return that result of the evaluation."

        "Give me a PDF version of notebook with id "222""


Resource Attributes
-------------------


- Cookie holds Session info
- 'avatarid' is the unique id of user requesting some `Action`
- Typically an SQL operation occurs
- State change: response is 'success' or 'fail'
- Data request: response is HTML, JSON, Image, PDF, XML, etc


Resources and their relation to an `Avatar`
===========================================

- Avatar holds User `Capabilities` i.e. what data
  the can view, change, delete and what state they can change.
