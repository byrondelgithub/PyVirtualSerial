import atexit
import ctypes
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal
from urllib.request import urlretrieve
from zipfile import ZipFile

from loguru import logger

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
    print(__version__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

if 'sphinx' not in sys.modules:
    from pyvirtualserial import *
###############################################################################################################


OS_NAME: Literal["posix", "nt"] = os.name
SETUP_PATH: Path | None = None
COM0COM_VERION: str = "2.2.2.0"

logger.remove()  # remove the old handler. Else, the old one will work along with the new one you've added below'
logger.add(sys.stdout, level="INFO")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_for_com0com():
    setup_path = Path(f"{os.environ['ProgramFiles(x86)']}\com0com\setupc.exe")
    is_installed = setup_path.exists()

    if is_installed:
        return setup_path

    logger.warning(
        f"com0com couldnt be found, installing version {COM0COM_VERION} from sourceforge..."
    )
    with TemporaryDirectory() as tempdir:
        file_handle, _ = urlretrieve(
            f"https://downloads.sourceforge.net/project/com0com/com0com/{COM0COM_VERION}/com0com-{COM0COM_VERION}-x64-fre-signed.zip"
        )
        zf = ZipFile(file_handle)
        zf.extractall(tempdir)
        subprocess.call(
            [f"{tempdir}\\com0com-{COM0COM_VERION}-x64-fre-signed\\setup.exe", "/S"]
        )
        logger.success("com0com successfully installed!")
    return setup_path


if OS_NAME != "posix" and 'sphinx' not in sys.modules:
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    atexit.register(lambda: input("Press enter to exit..."))
    SETUP_PATH = check_for_com0com()
