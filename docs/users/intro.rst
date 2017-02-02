.. _introduction:

Introduction 
------------

Overview
========

Pyticketswitch is a wrapper around Ingresso's F13 API.

Full API documentation (and a much better introduction) to can be found here: 

http://ingresso-group.github.io/slate/#introduction

The work horse of this wrapper is the wonderful 
`requests <http://docs.python-requests.org>` library.


Goals
=====

These are some general goals that we are aiming at. If you feel that something
overly complicates matters or doesn't meat these goals feel free to call us out
on it.

* Wrappers should be relatively logic free and generally light weight.
* It's OK to sanitise where necessary.
* Objects should be as extensible as possible and have nothing hidden away
  in private methods.
* Things should be presented in native formats where possible.
* If we don't have the data we will return None not empty lists or dictionaries
* No logic in __init__'s.
* Well tested and documented.

Licence
=======

Pyticketswitch is released under the MIT licence:

Copyright 2017 Ingresso Group LTD

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


