.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/pyvirtualserial.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/pyvirtualserial
    .. image:: https://readthedocs.org/projects/pyvirtualserial/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://pyvirtualserial.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/pyvirtualserial/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/pyvirtualserial
    .. image:: https://img.shields.io/pypi/v/pyvirtualserial.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/pyvirtualserial/
    .. image:: https://img.shields.io/conda/vn/conda-forge/pyvirtualserial.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/pyvirtualserial
    .. image:: https://pepy.tech/badge/pyvirtualserial/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/pyvirtualserial
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/pyvirtualserial

===============
pyvirtualserial
===============


    Library to create virtual serial ports on Windows and Linux.

On Windows Com0Com and admin permissions are needed. Using the library will ask you for elevation and install Com0Com for you if needed.
On Linux It uses the pty native library, simple as always.

Virtual serial creates a pair of virtual serials, anything sent to the master will be received in the slave and viceversa.

************
Installation
************
``pip install PyVirtualSerial``

*****
Usage
*****
Using Virtual serial is pretty simple, here is a simple script to create an echo Serial:
::

    from pyvirtualserial import VirtualSerial

    virtual_serial = VirtualSerial(timeout=60)
    while True:
        b = virtual_serial.read(1)
        virtual_serial.write(b)

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
