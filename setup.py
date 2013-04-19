from setuptools import setup, find_packages

version = '0.1'

setup(name='viper',
      version=version,
      description="",
      long_description=open('README.rst').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='N\xc3\xa9stor Salceda',
      author_email='nestor.salceda@gmail.com',
      url='',
      license='MIT/X11',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'tornado',
          'pymongo',
          'docutils',
          'pyDoubles==1.4',
          'nose',
          'pyhamcrest'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
