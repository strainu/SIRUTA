from distutils.core import setup
import distutils.command.install_data
import sys
import os

data_path = os.path.join(sys.prefix, 'sirutalib')

class custom_install_data(distutils.command.install_data.install_data):
    """need to change self.install_dir to the actual library dir"""
    def run(self):
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return distutils.command.install_data.install_data.run(self)


setup(name='SIRUTAlib',
      version='1.0',
      author='Andrei Cipu',
      author_email='siruta@strainu.ro',
      url='http://proiecte.strainu.ro/siruta/',
      license='3-clause BSD',
      py_modules=['sirutalib'],
      data_files=[
          ('', ['siruta.csv']),
          ],
      cmdclass = { 'install_data':    custom_install_data },
      )
