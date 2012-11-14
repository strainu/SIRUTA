from distutils.core import setup
import sys
import os

setup(name='SIRUTAlib',
      version='1.0',
      author='Andrei Cipu',
      author_email='siruta@strainu.ro',
      url='http://proiecte.strainu.ro/siruta/',
      license='3-clause BSD',
      py_modules=['sirutalib'],
      data_files=[
          (os.path.join(sys.prefix,'sirutalib'), ['siruta.csv','README.rst','INSTALL.rst','doc/help.html']),
          ],
      )
