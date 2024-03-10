"""
File with the base of a Virtual Serial for Linux that uses pty and tty

References:
    - https://docs.python.org/es/3/library/tty.html
    - https://docs.python.org/es/3.10/library/pty.html
"""

from pyvirtualserial import OS_NAME

if OS_NAME == "posix":
    import os, pty, tty, termios
from loguru import logger

__author__ = "byrondelgithub"
__copyright__ = "byrondelgithub"
__license__ = "MIT"


class LinuxBaseVirtualSerial:
    """
    Base class for Virtual Serials in linux that uses the tool pty to create a
    master file and slave serial.

    The master file is used to communicate with the user, anything sent to the master
    will be also sent to the slave and viceversa.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Linux virtual serials dont need baudrate, ports or timeout.
        To access the slave port name please use the function :func:`get_slave_name`
        """
        self._master: int = None
        self._slave: int = None
        self.__create_serial()

    def __create_serial(self):
        master, slave = pty.openpty()  # Create the pair
        tty.setraw(master, termios.TCSANOW)
        self._master = master
        self._slave = slave
        self._writer = os.fdopen(self._master, "wb")  # Create the writer for the master
        self._reader = os.fdopen(self._master, "rb")  # Create the reader for the master
        logger.debug(f"Creating virtual port at {self.get_slave_name()}")

    def get_slave_name(self) -> str:
        """
        Returns the slave serial port name

        Returns:
            str: Name of the slave serial port
        """
        return os.ttyname(self._slave)
