"""Setup script for redux-py"""

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

# The directory containing this file
HERE = abspath(dirname(__file__))

# The text of the README file
with open(join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="redux-py",
    version="0.1.0",
    description="Redux implementation for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Carsten-Leue/ReduxPY",
    author="Dr. Carsten Leue",
    author_email="carsten.leue@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["rx"],
    entry_points={"console_scripts": ["reduxpy=redux.__main__:main"]},
)
