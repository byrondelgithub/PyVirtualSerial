"""
File with the base of a Virtual Serial for Windows that uses Com0Com to work

References:
    - https://com0com.sourceforge.net
"""

import subprocess
import time
from loguru import logger
from serial import Serial
from pyvirtualserial.utils.com0com import SETUP_PATH
from pyvirtualserial.utils.context_managers import cd

__author__ = "byrondelgithub"
__copyright__ = "byrondelgithub"
__license__ = "MIT"


class WindowsBaseVirtualSerial:
    """
    Base class for Virtual Serials in windows that uses the tool Com0Com to create a
    slave/master pair of serials at port COM999 and COM``port``.

    The master serial is used to communicate with the user, anything sent to the master
    will be also sent to the slave and viceversa.
    """

    def __init__(
        self, port: int = 4000, baudrate: int = 9600, timeout = 5
    ) -> None:
        """
        Args:
            port (int, optional): Slave port used by the user, ports number in windows should be between the range of 2 and 4095. Defaults to 4000.
            baudrate (int, optional): Baudrate of the communication. Defaults to 9600.
            timeout (int, optional): Time before the Serial sends a ``TimeoutException`` when reading. Defaults to 5.
        """
        if port < 1 or port > 4095:
            raise Exception("The port must be between 2 and 4095")
        self._writer: Serial = None
        self._reader: Serial = None
        self.__port: int = port
        self.__baudrate: int = baudrate
        self._timeout: int = timeout
        self.__create_serial()

    def __create_serial(self):
        with cd(SETUP_PATH.parent):  # Move to the Com0Com setup path
            subprocess.run(
                [SETUP_PATH, "remove", "0"]
            )  # Remove the pair 0 if it exists
            logger.debug(f"Creating virtual port at COM{self.__port}")
            subprocess.call(  # Create the pair at COM# (master) and COM# (slave)
                [
                    SETUP_PATH,
                    "install",
                    "PortName=COM#,EmuBr=yes",
                    "PortName=COM#,EmuBr=yes",
                ]
            )
            time.sleep(0.5)
            subprocess.call(  # Changes the master port to 4096
                [
                    SETUP_PATH,
                    "change",
                    "CNCA0",
                    "RealPortName=COM4096",
                ]
            )
            subprocess.call(  # Changes the slave port to {self.__port}
                [
                    SETUP_PATH,
                    "change",
                    "CNCB0",
                    f"RealPortName=COM{self.__port}",
                ]
            )
        self._writer = Serial(
            "COM4096", baudrate=self.__baudrate
        )
        self._reader = self._writer

    def get_slave_name(self) -> str:
        """
        Returns the slave serial port name

        Returns:
            str: Name of the slave serial port
        """
        return f"COM{self.__port}"

    def read(self, bytes: int = 1) -> bytes:
        b = self._reader.read(bytes)
        logger.debug(f"Reading {b}")
        return b

    def readline(self) -> bytes:
        line = self._reader.readline()
        logger.debug(f"Reading line {line}")
        return line

    def readlines(self) -> list[bytes]:
        lines = self._reader.readlines()
        logger.debug(f"Reading lines {lines}")
        return lines

    def read_until(self, expected) -> bytes:
        response = self._reader.read_until(expected)
        logger.debug(f"Reading {response}")
        return response
    
    def read_all(self) -> bytes:
        response = self._reader.read_all()
        logger.debug(f"Reading all {response}")
        return response
    
    @property
    def timeout(self) -> int:
        return self._timeout
    
    @timeout.setter
    def timeout(self, timeout:int) -> None:
        self._timeout = timeout
        self._reader.timeout = timeout