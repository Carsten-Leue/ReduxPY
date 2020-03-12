import unittest
from os.path import dirname
from redux import create_store

# Current directory
HERE = dirname(__file__)

def test_store():
    print("Carsten", create_store)
    pass