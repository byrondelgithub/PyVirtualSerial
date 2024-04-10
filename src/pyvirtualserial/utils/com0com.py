import atexit
import ctypes
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

from loguru import logger

COM0COM_URL = "https://downloads.sourceforge.net/project/com0com/com0com/3.0.0.0/com0com-3.0.0.0-i386-and-x64-signed.zip"

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
        f"com0com couldnt be found, installing from sourceforge..."
    )
    with TemporaryDirectory() as tempdir:
        file_handle, _ = urlretrieve(
            COM0COM_URL
        )
        zf = ZipFile(file_handle)
        zf.extractall(tempdir)
        subprocess.call(
            [f"{tempdir}\\Setup_com0com_v3.0.0.0_W7_x64_signed.exe", "/S"]
        )
        logger.success("com0com successfully installed!")
    return setup_path

if os.name != "posix" and 'sphinx' not in sys.modules:
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    atexit.register(lambda: input("Press enter to exit..."))
    SETUP_PATH = check_for_com0com()