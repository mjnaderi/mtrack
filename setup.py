import os
from mtrack import version
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mtrack',
    version=version.__version__,
    description='My simple time tracker',
    long_description=README,
    author='Mohammad Javad Naderi',
    url='https://github.com/mjnaderi/mtrack',
    packages=find_packages(),
    include_package_data=True,
    scripts=['mtrack/mtrack'],
    install_requires=[
        'sh', 'pony', 'pytz', 'tzlocal'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
