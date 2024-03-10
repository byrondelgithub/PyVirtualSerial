"""Custom context managers for pyvirtualserial"""

import os

__author__ = "byrondelgithub"
__copyright__ = "byrondelgithub"
__license__ = "MIT"


class cd:
    """Context manager for cd operations"""

    def __init__(self, new_path) -> None:
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, *args):
        os.chdir(self.saved_path)
