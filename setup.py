from setuptools import setup

setup(name='thrift_http_tornado',
      version='0.1.1',
      description='Thirft transport implementation over the HTTP protocol',
      author='Alexis Montagne',
      author_email='alexis.montagne@upfluence.co',
      url='https://github.com/upfluence/thrift-http-tornado',
      packages=['thrift_http_tornado'],
      install_requires=['thrift', 'tornado', 'futures', 'toro'])
