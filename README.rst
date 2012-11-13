This project aims to create a library that can import a `SIRUTA <http://colectaredate.insse.ro/senin/classifications.htm?selectedClassification=&action=&classificationName=SIRUTA&classificationVersion=Versiune>`_ database and offer simple access to the different elements of the database.

What is SIRUTA?
===============
`SIRUTA <http://colectaredate.insse.ro/senin/classifications.htm?selectedClassification=&action=&classificationName=SIRUTA&classificationVersion=Versiune>`_ is the official clasification of the Romanian towns and villages (hereafter called entity). It is maintained by the `National Statistics Institute <http://www.insse.ro/>`_.

It gives every entity a 6 digit code (5-digit unique code and 1-digit checksum). The whole classification is hierachical, with Romania (the country) as root, then 40 counties + Bucharest. Bucharest contains the city of Bucharest, which in turn contains 6 sectors. Every county has municipalities, citiess and communes, and each of those is comprised of towns and villages.

The SIRUTA archives contain detailed documentation about the whole classification, including the algoritm for the checksum. 

.. note::
    This library makes the assumption that SIRUTA codes shorter than 6 characters are filled with 0 to the left in order to calculate the checksum. There are 77 codes that do not respect this assumpsion. Out of those, 76 can be calculated if the code is filled with 0's to the *right*. The remaining code is 9026.

Install
=======

.. include:: INSTALL.rst


Development
===========
To work on the PubDocs code, you only need a local repository checkout::

    $ git clone https://github.com/strainu/SIRUTA.git
    $ cd siruta

That's it, enjoy!
