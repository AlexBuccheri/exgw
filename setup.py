from setuptools import setup

setup(name='exgw',
      version='0.0.1',
      description='GW calcs',
      author='Alex Buccheri',
      author_email='abuccheri@physik.hu-berlin.de',
      packages=['exgw'],
      include_package_data=True,
      install_requires=[
          'numpy>=1.14.5',
          'matplotlib>=2.2.0'],
      )
