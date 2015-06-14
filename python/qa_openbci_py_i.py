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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from openbci_py_i import openbci_py_i
import time

class qa_openbci_py_i(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        src = None#openbci_py_i("test")
        snk = blocks.vector_sink_i()
        self.tb.connect(src, snk)
        #self.tb.run()
        self.tb.start(256)
        time.sleep(0.001)
        self.tb.stop()
        self.tb.wait()
        # check data
        expected_result = [1] * 256
        result_data = snk.data()
        #print(result_data)
        self.assertFloatTuplesAlmostEqual(expected_result, result_data[:256], 256)

if __name__ == '__main__':
    gr_unittest.run(qa_openbci_py_i, "qa_openbci_py_i.xml")
