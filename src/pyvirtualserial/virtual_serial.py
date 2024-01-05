import subprocess
import sys
import os
import time
from . import SETUP_PATH


class cd:
    """Context manager for cd operations"""

    def __init__(self, new_path) -> None:
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, *args):
        os.chdir(self.saved_path)


with cd(SETUP_PATH.parent):
    subprocess.Popen(
        [
            SETUP_PATH,
            "install",
            "PortName=COM#,EmuBr=yes",
            "PortName=COM#,EmuBr=yes",
        ]
    )
    time.sleep(5)
    subprocess.run([SETUP_PATH, "remove", "0"])


class VirtualSerial:
    def __init__(
        self,
        threaded: bool = False,
        start_cmd: str | None = None,
        stop_cmd: str | None = None,
    ) -> None:
        self.__is_threaded = threaded
        self.__start_cmd = start_cmd
        self.__stop_cmd = stop_cmd

        self._serial_name: str = None

    def create_serial(self):
        pass

    @property
    def is_threaded(self):
        return self.__is_threaded

    @property
    def serial_name(self):
        return self.__is_threaded
