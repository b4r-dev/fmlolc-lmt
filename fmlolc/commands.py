# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# public items
__all__ = ['initialize',
           'start_fm',
           'stop_fm',
           'finalize']

# standard library
from logging import getLogger

# dependent packages
import fmlolc

# module logger
logger = getLogger(__name__)


# functions
def initialize(fmp_file, lo_freq, multiply=8):
    """Initialize 1st LO SG and XFFTS for FM mode.

    Args:
        fmp_file (str or path): Path of FM pattern file.
        lo_freq (float): LO frequency at FM frequency = 0 in units of GHz.
        multiply (int): Multiplication factor of SG-to-LO frequency.

    """
    listfreq = fmlolc.listfreq(fmp_file, lo_freq, multiply)

    with fmlolc.SCPI(**fmlolc.INFO_XFFTS) as xffts:
        xffts('XFFTS:CMDUSEDSECTIONS 1 1 1 1')
        xffts('XFFTS:CMDSYNCTIME 200000')
        xffts('XFFTS:CMDBLANKTIME 5000')
        xffts('XFFTS:CONFIG')

    with fmlolc.SCPI(**fmlolc.INFO_SG) as sg:
        sg('FREQ:MODE CW')
        sg('OUTP ON')
        sg('INIT:CONT OFF')
        sg('LIST:TYPE LIST')
        sg('LIST:DWEL 2.0E-01')
        sg('LIST:TRIG:SOUR EXT')
        sg('FREQ:MODE LIST')
        sg('TRIG:SLOP POS')

        # this must be the last
        sg('LIST:FREQ {0}'.format(listfreq))


def start_fm():
    """Start FM mode."""
    with fmlolc.SCPI(**fmlolc.INFO_XFFTS) as xffts:
        # spacify commands if necessary
        pass

    with fmlolc.SCPI(**fmlolc.INFO_SG) as sg:
        sg('INIT:CONT ON')


def stop_fm():
    """Stop FM mode."""
    with fmlolc.SCPI(**fmlolc.INFO_XFFTS) as xffts:
        # spacify commands if necessary
        pass

    with fmlolc.SCPI(**fmlolc.INFO_SG) as sg:
        # spacify commands if necessary
        pass

    finalize()


def finalize():
    """Revert 1st LO SG and XFFTS to non FM mode."""
    with fmlolc.SCPI(**fmlolc.INFO_XFFTS) as xffts:
        xffts('XFFTS:CMDUSEDSECTIONS 1 1 1 1')
        xffts('XFFTS:CMDSYNCTIME 200000')
        xffts('XFFTS:CMDBLANKTIME 1000')
        xffts('XFFTS:CONFIG')

    with fmlolc.SCPI(**fmlolc.INFO_SG) as sg:
        sg('FREQ:MODE CW')
        sg('LIST:FREQ 1.75E+10')
        sg('LIST:TRIG:SOUR IMM')
