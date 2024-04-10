import sys

from loguru import logger

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from pyvirtualserial.virtual_serial import *
###############################################################################################################

logger.remove()  # remove the old handler. Else, the old one will work along with the new one you've added below'
logger.add(sys.stdout, level="INFO")
