import setuptools
from distutils.core import setup
import distutils.command.install_data
import pathlib
import sys
import os

data_path = os.path.join(sys.prefix, 'sirutalib')

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


class custom_install_data(distutils.command.install_data.install_data):
    """need to change self.install_dir to the actual library dir"""
    def run(self):
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        self.data_files = [('', ['siruta.csv'])]
        return distutils.command.install_data.install_data.run(self)


setup(name='sirutalib',
      version='1.3.0',
      author='Andrei Cipu',
      author_email='siruta@strainu.ro',
      description="Work with the Romanian settlement database, SIRUTA",
      long_description=README,
      long_description_content_type="text/markdown",
      url='http://proiecte.strainu.ro/siruta/',
      license='3-clause BSD',
      py_modules=['sirutalib'],
      data_files=[
          ('', ['siruta.csv', 'README.rst', 'doc/help.html']),
      ],
      cmdclass={'install_data': custom_install_data},
      setup_requires=['wheel']
      )
