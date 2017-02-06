.. _introduction:

Introduction 
------------

Overview
========

Pyticketswitch is a wrapper around Ingresso's F13 API.

Full API documentation (and a much better introduction) can be found here: 

http://ingresso-group.github.io/slate/

The work horse of this wrapper is the wonderful 
`Requests`_ library.

.. _`Requests`: http://docs.python-requests.org

Goals
=====

These are some general goals that we are aiming at. If you feel that something
overly complicates matters or doesn't meet these goals feel free to call us out
on it.

* Wrappers should be relatively logic free and generally light weight.
* It's OK to sanitise where necessary.
* Objects should be as extensible as possible and have nothing hidden away
  in private methods.
* Things should be presented in native formats where possible.
* If we don't have the data we will return None not empty lists or dictionaries
* No logic in __init__'s.
* Well tested and documented.
* Python 3 primary target with python 2 support

Legacy API
==========

Prior to version 2.0.0 this wrapper dealt with the ticketswitch XML API. This
library was a horrible mess and we have remodeled and restructured it beyond
the point of recognition (actually we deleted everything and started again).

As such if you are looking to interact with the XML API then the last release
of this library supporting it was version 1.13.0. 
:ref:`See legacy installation instructions <legacy_install>`

We do not intended to reintroduce support for this API and will eventually take
it out of circualation, however there is no date set for this as of yet.


Licence
=======

    .. include:: ../../LICENSE
