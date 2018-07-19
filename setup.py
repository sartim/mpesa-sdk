from setuptools import setup

setup(name='mpesa-api-sdk',
      version='0.1',
      description='M-Pesa API SDK',
      url='https://github.com/sartim/mpesa-python-sdk',
      author='sartim',
      author_email='sarrtim@gmail.com',
      license='MIT',
      packages=['mpesa'],
      install_requires=[
          'requests',
      ],
      dependency_links=['https://github.com/sartim/mpesa-python-sdk/master#egg=package-1.0'],
      zip_safe=False)
