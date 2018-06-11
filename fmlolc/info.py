# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# public items
__all__ = ['INFO_SG',
           'INFO_XFFTS']

# standard library
from logging import getLogger

# module logger
logger = getLogger(__name__)


# module constants
INFO_SG = {'host': '',
           'port': '',
           'protocol': 'TCP'}

INFO_XFFTS = {'host': '',
              'port': '',
              'protocol': 'UDP'}
