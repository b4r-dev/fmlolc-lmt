# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# public items
__all__ = ['SCPI',
           'listfreq']

# standard library
import time
from logging import getLogger
from socket import socket, timeout
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM

# dependent packages
import numpy as np
from pathlib2 import Path

# module logger
logger = getLogger(__name__)


# classes
class SCPI(object):
    def __init__(self, host, port, protocol, timeout=0.1,
                 buffersize=4096, linebreak='\r\n'):
        """Create SCPI interface for instrument.

        Args:
            host (str): IP address of instrument.
            port (int or str): Port number of instrument.
            protocol (str): Transport protocol. Must be either 'TCP' or 'UDP'.
            timeout (float): Connection timeout in units of sec. Default is 0.1.
            buffersize (int): Byte size for receiving data. Default is 4096.
            linebreak (str): Line break string. Default is '\r\n' (CRLF).

        Example:
            >>> sg = SCPI('192.168.1.2', 8000, 'TCP')

            >>> sg('FREQ 10')
            SEND> FREQ 10

            >>> sg('FREQ?')
            SEND> FREQ?
            RECV> 10

        """
        self.address    = (host, int(port))
        self.protocol   = protocol
        self.timeout    = timeout
        self.buffersize = buffersize
        self.linebreak  = linebreak

        if self.protocol == 'TCP':
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(self.address)
        elif self.protocol == 'UDP':
            self.socket = socket(AF_INET, SOCK_DGRAM)
        else:
            raise ValueError(self.protocol)

        self.socket.settimeout(self.timeout)

    def __call__(self, command):
        """Send SCPI command.

        Args:
            command (str): SCPI command. If it ends with '?',
                this method automatically receives message.

        Returns:
            recvdata (str): Received data (if any).

        """
        logger.info('SEND> {0}'.format(command))
        senddata = str(command) + self.linebreak

        if self.protocol == 'TCP':
            self.socket.send(senddata)
        elif self.protocol == 'UDP':
            self.socket.sendto(senddata, self.address)
        else:
            raise ValueError(self.protocol)

        recvdata = self.recv()
        logger.info('RECV> {0}'.format(recvdata))
        return recvdata

    def recv(self):
        """Receive data until timeout exception is raised."""
        recvdata = ''

        while True:
            try:
                recvdata += self.socket.recv(self.buffersize)
            except timeout:
                return recvdata

    def __enter__(self):
        """Special method for with statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Special method for with statement."""
        self.socket.close()


# functions
def listfreq(fmp_file, lo_freq, lo_multiply=8):
    """Create frequency list for SCPI command.

    Args:
        fmp_file (str or path): Path of FM pattern file.
        lo_freq (float): LO frequency at FM frequency = 0 in units of GHz.
        lo_multiply (int): Multiplication factor of SG-to-LO frequency.

    Returns:
        listfreq (str): String of series of SG frequencies in units of Hz.

    """
    path = str(Path(fmp_file).expanduser())
    fm_freq = np.loadtxt(path, usecols=(1,))
    sg_freq = (fm_freq + 1e9*lo_freq) / lo_multiply

    return ','.join('{0:.9E}'.format(f) for f in sg_freq)
