# coding: utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# public items
__all__ = ['SCPI']

# standard library
from socket import socket, AF_INET, SOCK_STREAM
from logging import getLogger

# dependent packages
from pathlib2 import Path

# module logger
logger = getLogger(__name__)


# classes
class SCPI(socket):
    """Create an interface to SCPI instruments.

    Args:
        host (str): IP address of the instrument.
        port (int): Port number of the instrument.
        encoding (str): Data encoding. Default is 'ascii'.

    Example:
        >>> FG = SCPI('192.168.1.2', port=8000)
        >>> FG.send('FREQ 10')

    """
    def __init__(self, host, port=8000, encoding='ascii'):
        self.host = host
        self.port = port
        self.encoding = encoding

        super(SCPI, self).__init__(AF_INET, SOCK_STREAM)
        self.connect((host, port))

    def send(self, command):
        # send data as bytes
        senddata = '{0}\n'.format(command).encode(self.encoding)
        logger.info('SEND> {0}'.format(command))
        super(SCPI, self).send(senddata)

        # receive data (if necessary)
        if command.endswith('?'):
            recvdata = self.recv(1024).decode(self.encoding)
            logger.info('RECV> {0}'.format(recvdata))

    def reset(self):
        self.send('*RST')
        self.send('*CLS')
