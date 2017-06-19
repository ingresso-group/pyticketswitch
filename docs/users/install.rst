.. _install:

Installation 
------------

Pyticketswitch is distributed via `Pypi`_ and is available open source on 
`Github`_.


.. _`Pypi`: https://pypi.python.org/pypi/pyticketswitch/
.. _`Github`: https://github.com/ingresso-group/pyticketswitch/

Pip install
===========

To install pyticketswitch simply type this into your terminal::

    $ pip install pyticketswitch

If you don't have `pip <https://pip.pypa.io>`_ installed,
`this Python installation guide <http://docs.python-guide.org/en/latest/starting/installation/>`_
can guide you through the process.

We recomend working in virtual enviroment to isolate your projects requirements
from other python programs running on your system. 
`Here is a good guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

Source code
===========

You can either clone the public repository::

    $ git clone git://github.com/ingresso-group/pyticketswitch.git

Or, download the tarball::

    $ curl -OL https://github.com/ingresso-group/pyticketswitch/tarball/master

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ python setup.py install


Legacy Versions
===============

.. _legacy_install:


The last version of this wrapper that supported the old XML API was version
`1.13.0 <https://github.com/ingresso-group/pyticketswitch/releases/tag/1.13.1>`_.
Any future bug fixes for the XML wrapper will be on the 
`stable/v1.x <https://github.com/ingresso-group/pyticketswitch/tree/stable/v1.x>`_
branch.

To install this version specifically via pip::

    $ pip install pyticketswitch==1.13.1

Or, download the tarball::

    $ curl -OL https://github.com/ingresso-group/pyticketswitch/archive/1.13.1.tar.gz
