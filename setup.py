from setuptools import setup, find_packages

setup(name='prototapes',
      version='0.001',
      description='music sharing website',
      author='Some dudes',
      package_dir={'':'src'},
      packages=find_packages('src'),
      test_suite='tests'
     )