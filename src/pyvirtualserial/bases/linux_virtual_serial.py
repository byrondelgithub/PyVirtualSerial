"""
File with the base of a Virtual Serial for Linux that uses pty and tty

References:
    - https://docs.python.org/es/3/library/tty.html
    - https://docs.python.org/es/3.10/library/pty.html
"""
import os
import time
from select import select

if os.name == "posix":
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

    def __init__(self, timeout = 5, *args, **kwargs) -> None:
        """
        Linux virtual serials dont need baudrate, ports or timeout.
        To access the slave port name please use the function :func:`get_slave_name`
        """
        self._timeout: int = timeout
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

    def read(self, bytes: int = 1) -> bytes:
        b = b""
        while len(b) < bytes:
            rlist, _, _ = select([self._reader], [], [], self.timeout)
            if rlist:
                b += self._reader.read1(1)
            else:
                break
        logger.debug(f"Reading {b}")
        return b

    def read_until(self, expected) -> bytes:
        b = b""
        s_time = time.time()
        while b[-len(expected):] != expected :
            if self._timeout is not None and time.time() - s_time >= self._timeout:
                break
            b += self.read(1)
        logger.debug(f"Reading {b}")
        return b
    
    def readline(self) -> bytes:
        line = self.read_until(b"\n")
        logger.debug(f"Reading line {line}")
        return line

    def readlines(self) -> list[bytes]:
        lines = self._reader.readlines()
        logger.debug(f"Reading lines {lines}")
        return lines
    
    def read_all(self) -> bytes:
        response = b""
        rlist, _, _ = select([self._reader], [], [], 0)
        if rlist:
            response = self._reader.read1()
        logger.debug(f"Reading all {response}")
        return response

    def get_slave_name(self) -> str:
        """
        Returns the slave serial port name

        Returns:
            str: Name of the slave serial port
        """
        return os.ttyname(self._slave)

    @property
    def timeout(self) -> int:
        return self._timeout
    
    @timeout.setter
    def timeout(self, timeout:int) -> None:
        self._timeout = timeout