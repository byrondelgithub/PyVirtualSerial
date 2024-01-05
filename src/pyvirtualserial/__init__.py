import sys, os, ctypes
from elevate import elevate
from pathlib import Path
from loguru import logger

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
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

###############################################################################################################


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_for_com0com():
    setup_path = Path(f"{os.environ['ProgramFiles(x86)']}\com0com\setupc.exe")
    is_installed = setup_path.exists()

    if not is_installed:
        # create terminal and save the file to path
        return

    return setup_path


SETUP_PATH: Path | None = None

if os.name != "posix":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        print(" ".join(sys.argv))
        sys.exit()
    SETUP_PATH = check_for_com0com()
