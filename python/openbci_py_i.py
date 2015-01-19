#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
import open_bci_v3 as bci

class openbci_py_i(gr.sync_block):
    """
    docstring for block openbci_py_i
    """
    def __init__(self, port):
        gr.sync_block.__init__(
            self,
            name = "openbci_py_i",
            in_sig = None,
            out_sig = [numpy.int32])
        self.port = port
        #self.set_output_multiple(256)

        # init openbci dongle
        self.board = None
        self.sampleid = -1
        if port != "test":
            self.board = bci.OpenBCIBoard(port=port,scaled_output=False)
            self.board.ser.write('b')
            self.board.streaming = True
        print "init openbci_py_i ", port

    def __del__(self):
        if self.board is not None:
            self.board.stop()
            self.board.disconnect()
            del self.board
            self.board = None
        gr.sync_block.__del__(self)
        print "del openbci_py_i"

    def work(self, input_items, output_items):
        out = output_items[0]
        n = len(out)

        # qa test output
        if self.board is None:
            out[:] = [1]*n
            return n

        # populate output
        for i in xrange(n):
            sample = self.board._read_serial_binary()
            if self.sampleid > -1:
                if ((self.sampleid+1)%256) != sample.id:
                    print "missed sample #", sample.id
            self.sampleid = sample.id
            out[i] = sample.channel_data[0]

        return n
