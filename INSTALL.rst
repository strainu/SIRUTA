Installation
============
In order to install SIRUTAlib, you just need to extract the archive and run the following command (usually as root): 

::

    # python setup.py install


Then, you can just import sirutalib in your program::
    #!/usr/bin/python
    import sirutalib

    if __name__ == "__main__":
        siruta = sirutalib.SirutaDatabase()
        print siruta.get_name(10)#10 is the SIRUTA code for Alba county

