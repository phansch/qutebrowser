# Copyright 2014-2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for qutebrowser.utils.debug."""

import re
import time
import unittest
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle, QFrame

from qutebrowser.utils import debug
from qutebrowser.test import stubs


class TestDebug(unittest.TestCase):

    """Test signal debug output functions."""

    def setUp(self):
        self.signal = stubs.FakeSignal()

    def test_signal_name(self):
        """Test signal_name()."""
        self.assertEqual(debug.signal_name(self.signal), 'fake')

    def test_dbg_signal(self):
        """Test dbg_signal()."""
        self.assertEqual(debug.dbg_signal(self.signal, [23, 42]),
                         'fake(23, 42)')

    def test_dbg_signal_eliding(self):
        """Test eliding in dbg_signal()."""
        self.assertEqual(debug.dbg_signal(self.signal,
                                          ['x' * 201]),
                         "fake('{}\u2026)".format('x' * 198))

    def test_dbg_signal_newline(self):
        """Test dbg_signal() with a newline."""
        self.assertEqual(debug.dbg_signal(self.signal, ['foo\nbar']),
                         r"fake('foo\nbar')")


class TestLogTime(unittest.TestCase):

    """Test log_time."""

    def test_log_time(self):
        """Test if log_time logs properly."""
        logger = logging.getLogger('qt-tests')
        with self.assertLogs(logger, logging.DEBUG) as logged:
            with debug.log_time(logger, action='foobar'):
                time.sleep(0.1)
            self.assertEqual(len(logged.records), 1)
            pattern = re.compile(r'^Foobar took ([\d.]*) seconds\.$')
            match = pattern.match(logged.records[0].msg)
            self.assertTrue(match)
            duration = float(match.group(1))
            self.assertAlmostEqual(duration, 0.1, delta=0.01)

if __name__ == '__main__':
    unittest.main()
