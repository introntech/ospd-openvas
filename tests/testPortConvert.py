# $id$
# description:
# Test suites for Port manipulation.
#
# authors:
#   Juan Jose Nicola <juan.nicola@greenbone.net>
#
# copyright:
# copyright (c) 2018 greenbone networks gmbh
#
# this program is free software; you can redistribute it and/or
# modify it under the terms of the gnu general public license
# as published by the free software foundation; either version 2
# of the license, or (at your option) any later version.
#
# this program is distributed in the hope that it will be useful,
# but without any warranty; without even the implied warranty of
# merchantability or fitness for a particular purpose.  see the
# gnu general public license for more details.
#
# you should have received a copy of the gnu general public license
# along with this program; if not, write to the free software
# foundation, inc., 51 franklin st, fifth floor, boston, ma 02110-1301 usa.
from __future__ import print_function

import unittest

from ospd.misc import ports_as_list
from ospd.misc import get_udp_port_list
from ospd.misc import get_tcp_port_list

class FullTest(unittest.TestCase):

    def testTcpPorts(self):
        """ Test only tcp ports."""
        tports, uports = ports_as_list('T:1-10,30,31')
        self.assertFalse(tports is None)
        self.assertEqual(len(uports), 0)
        self.assertEqual(len(tports), 12)
        for i in range(1, 10):
            self.assertTrue(i in tports)
        self.assertTrue(30 in tports)
        self.assertTrue(31 in tports)

    def testUdpPorts(self):
        """ Test only udp ports."""
        tports, uports = ports_as_list('U:1-10')
        self.assertFalse(uports is None)
        self.assertEqual(len(tports), 0)
        self.assertEqual(len(uports), 10)
        for i in range(1, 10):
            self.assertTrue(i in uports)

    def testBothPorts(self):
        """ Test tcp und udp ports."""
        tports, uports = ports_as_list('T:1-10, U:1-10')
        self.assertFalse(tports is None)
        self.assertFalse(uports is None)
        self.assertEqual(len(tports), 10)
        self.assertEqual(len(uports), 10)
        for i in range(1, 10):
            self.assertTrue(i in tports)
            self.assertTrue(i in uports)
        self.assertFalse(0 in uports)

    def testBothPortsUdpfirst(self):
        """ Test tcp und udp ports, but udp listed first."""
        tports, uports = ports_as_list('U:20-30, T:1-10')
        self.assertFalse(tports is None)
        self.assertFalse(uports is None)
        self.assertEqual(len(tports), 10)
        self.assertEqual(len(uports), 11)
        for i in range(1, 10):
            self.assertTrue(i in tports)
        for i in range(20, 30):
            self.assertTrue(i in uports)

    def testNotSpecTypePorts(self):
        """ Test port list without specific type. """
        tports, uports = ports_as_list('51-60')
        self.assertFalse(tports is None)
        self.assertEqual(len(uports), 0)
        self.assertEqual(len(tports), 10)
        for i in range(51, 60):
            self.assertTrue(i in tports)

    def testInvalidCharPort(self):
        """ Test list with a false char. """
        tports, uports = ports_as_list('R:51-60')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

    def testEmptyPort(self):
        """ Test an empty port list. """
        tports, uports = ports_as_list('')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

    def testGetSpecTypePorts(self):
        """ Test get specific type ports."""
        uports = get_udp_port_list('U:9392,9393T:22')
        self.assertEqual(len(uports), 2)
        self.assertTrue(9392 in uports)
        tports = get_tcp_port_list('U:9392T:80,22,443')
        self.assertEqual(len(tports), 3)
        self.assertTrue(22 in tports)
        self.assertTrue(80 in tports)
        self.assertTrue(443 in tports)

    def testMalformedPortStr(self):
        """ Test different malformed port list. """
        tports, uports = ports_as_list('TU:1-2')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

        tports, uports = ports_as_list('U1-2')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

        tports, uports = ports_as_list('U:1-2t:22')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

        tports, uports = ports_as_list('U1-2,T22')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)

        tports, uports = ports_as_list('U:1-2,U:22')
        self.assertTrue(tports is None)
        self.assertTrue(uports is None)
