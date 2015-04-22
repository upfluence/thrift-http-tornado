from setuptools import setup

setup(name='thrift_http_tornado',
      version='0.0.5',
      description='Thirft transport implementation over the HTTP protocol',
      author='Alexis Montagne',
      author_email='alexis.montagne@upfluence.co',
      url='https://github.com/upfluence/thrift-http-tornado',
      packages=['thrift_http_tornado'],
      install_requires=['thrift', 'tornado', 'futures', 'toro'])
