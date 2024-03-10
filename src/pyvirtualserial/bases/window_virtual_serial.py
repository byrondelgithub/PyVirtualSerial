"""
File with the base of a Virtual Serial for Windows that uses Com0Com to work

References:
    - https://com0com.sourceforge.net
"""

import subprocess
from loguru import logger
from serial import Serial
from pyvirtualserial import SETUP_PATH
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
        self, port: int = 10000, baudrate: int = 9600, timeout: int = 5
    ) -> None:
        """
        Args:
            port (int, optional): Slave port used by the user. Defaults to 10000.
            baudrate (int, optional): Baudrate of the communication. Defaults to 9600.
            timeout (int, optional): Time before the Serial sends a ``TimeoutException`` when reading. Defaults to 5.
        """
        self._writer: Serial = None
        self._reader: Serial = None
        self.__port: int = port
        self.__baudrate: int = baudrate
        self.__timeout: int = timeout
        self.__create_serial()

    def __create_serial(self):
        with cd(SETUP_PATH.parent):  # Move to the Com0Com setup path
            subprocess.run(
                [SETUP_PATH, "remove", "0"]
            )  # Remove the pair 0 if it exists
            logger.debug(f"Creating virtual port at COM{self.__port}")
            subprocess.call(  # Create the pair at COM999 (master) and COM{self.__port} (slave)
                [
                    SETUP_PATH,
                    "install",
                    "PortName=COM9999,EmuBr=yes",
                    f"PortName=COM{self.__port},EmuBr=yes",
                ]
            )
        self._writer = Serial(
            "COM9999", baudrate=self.__baudrate, timeout=self.__timeout
        )
        self._reader = self._writer

    def get_slave_name(self) -> str:
        """
        Returns the slave serial port name

        Returns:
            str: Name of the slave serial port
        """
        return f"COM{self.__port}"
