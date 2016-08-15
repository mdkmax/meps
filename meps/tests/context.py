import sys
import os

# Add path for test imports.
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from meps import meps
