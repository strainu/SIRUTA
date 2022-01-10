`This project <http://proiecte.strainu.ro/siruta/>`_ aims to create a library that can import a `SIRUTA <http://colectaredate.insse.ro/senin/classifications.htm?selectedClassification=&action=&classificationName=SIRUTA&classificationVersion=Versiune>`_ database and offer simple access to the different elements of the database.

What is SIRUTA?
===============
`SIRUTA <http://colectaredate.insse.ro/senin/classifications.htm?selectedClassification=&action=&classificationName=SIRUTA&classificationVersion=Versiune>`_ is the official clasification of the Romanian towns and villages (hereafter called entity). It is maintained by the `National Statistics Institute <http://www.insse.ro/>`_.

It gives every entity a 6 digit code (5-digit unique code and 1-digit checksum). The whole classification is hierachical, with Romania (the country) as root, then 40 counties + Bucharest. Bucharest contains the city of Bucharest, which in turn contains 6 sectors. Every county has municipalities, citiess and communes, and each of those is comprised of towns and villages.

The SIRUTA archives contain detailed documentation about the whole classification, including the algoritm for the checksum. 

.. note::
    This library makes the assumption that SIRUTA codes shorter than 6 characters are filled with 0 to the left in order to calculate the checksum. There are 77 codes that do not respect this assumption. Out of those, 76 can be calculated if the code is filled with 0's to the *right*. The remaining code is 9026.
    
Getting the library
===================

You can either `download the tar file <https://github.com/strainu/SIRUTA/releases/download/v1.2/SIRUTAlib-1.2.tar.gz>`_ (`mirror <http://proiecte.strainu.ro/siruta/SIRUTAlib-1.2.tar.gz>`_) or get the source code, as described in the :ref:`development-label` section.

In both cases, you will also get a copy of the most recent SIRUTA database in :abbr:`CSV (Comma-Separated Values)` format.

.. _development-label:

Development
===========
Dependencies
------------
 * a recent version of **python** is required in order to develop with SIRUTAlib
 * this library uses **Git** for source control, so you'll need that if you want to get the full source code. 
 * if you want to build the help files, you'll also need **sphinx** and **make** (the latter is optional)


Getting the source
------------------
To work on the SIRUTAlib code, you only need a local repository checkout::

    $ git clone https://github.com/strainu/SIRUTA.git
    $ cd siruta

You will find 2 python files:
 * ``sirutalib.py`` contains the actual library
 * ``testsiruta.py`` contains the tests needed to check the code.

That's it, enjoy!

Using the library
-----------------

A simple usage example is available in the INSTALL file.

Contributing
------------

If you plan to contribute code to SIRUTAlib, please keep a few things in mind:
 * code should be formatted according to :pep:`8`
 * tests should be written for all the new code, as long as you don't need to change class internals to test it
 
Then prepare a patch and submit a pull request on `github <https://github.com/strainu/SIRUTA/issues>`_.

For more contact options, see :ref:`contact-label`.

.. _contact-label:

Feedback and contact
====================

You can register a bug, feature request or pull request on github: https://github.com/strainu/SIRUTA/issues

If you want to contact the author, you can do it by emailing ``siruta [at] strainu.ro``. All the latest information is available on `the project's page <http://proiecte.strainu.ro/siruta/>`_.
