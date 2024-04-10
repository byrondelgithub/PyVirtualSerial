from loguru import logger
import os

__author__ = "byrondelgithub"
__copyright__ = "byrondelgithub"
__license__ = "MIT"

if os.name == "nt":
    from pyvirtualserial.bases.window_virtual_serial import (
        WindowsBaseVirtualSerial as BaseVirtualSerial,
    )
else:
    from pyvirtualserial.bases.linux_virtual_serial import (
        LinuxBaseVirtualSerial as BaseVirtualSerial,
    )


class VirtualSerial(BaseVirtualSerial):
    """
    Virtual serial compatible for both windows and linux.

    A virtual serial is uses a master serial to communicate with a slave serial,
    everything sent to the master will be received in the slave and viceversa.

    You can communicate with the slave serial using ``write``, ``read``, ``readline``, ``readline_CR`` and ``readlines``.

    Please check ``WindowsBaseVirtualSerial`` and ``LinuxBaseVirtualSerial`` for more information
    on how It works.
    """

    def __init__(
        self, port: int = 4000, baudrate: int = 9600, timeout: int = 5
    ) -> None:
        """
        At the moment you initialize this class the pair of serial ports will be created.

        Args:
            port (int, optional): Number of the serial port COM{port} (Only for windows). Defaults to 10000.
            baudrate (int, optional): Baudrate of the communication (Only for windows). Defaults to 9600.
            timeout (int, optional): Time before the Serial sends a ``TimeoutException`` when reading (Only for windows). Defaults to 5.
        """
        super().__init__(port, baudrate)
        self._timeout = timeout

    def write(self, bytes: bytes):
        logger.debug(f"Writing {bytes}")
        self._writer.write(bytes)
        self._writer.flush()

