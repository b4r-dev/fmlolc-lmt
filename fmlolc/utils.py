# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# public items
__all__ = ['SCPI']

# standard library
from logging import getLogger
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

# dependent packages
from pathlib2 import Path

# module logger
logger = getLogger(__name__)


# classes
class SCPI(object):
    def __init__(self, host, port, protocol):
        """Create SCPI interface for instrument.

        Args:
            host (str): IP address of instrument.
            port (int or str): Port number of instrument.
            protocol (str): Transport protocol. Must be either 'TCP' or 'UDP'.

        Example:
            >>> sg = SCPI('192.168.1.2', 8000, 'TCP')

            >>> sg('FREQ 10')
            SEND> FREQ 10

            >>> sg('FREQ?')
            SEND> FREQ?
            RECV> 10

        """
        self.address = (host, int(port))
        self.protocol = protocol

        if self.protocol == 'TCP':
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(self.address)
        elif self.protocol == 'UDP':
            self.socket = socket(AF_INET, SOCK_DGRAM)
        else:
            raise ValueError(protocol)

    def __call__(self, command):
        """Send SCPI command.

        Args:
            command (str): SCPI command. If it ends with '?',
                this method automatically receives message.

        """
        # send command as bytes
        logger.info('SEND> {0}'.format(command))
        senddata = command + '\r\n'

        if self.protocol == 'TCP':
            self.socket.send(senddata)
        elif self.protocol == 'UDP':
            self.socket.sendto(senddata, self.address)

        # receive message (if necessary)
        if command.endswith('?'):
            recvdata = self.socket.recv(8192)
            logger.info('RECV> {0}'.format(recvdata))

    def __enter__(self):
        """Special method for with statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Special method for with statement."""
        self.socket.close()
