# -*- coding: utf-8 -*-

# Copyright (c) 2012 Naoya INADA <naoina@kuune.org>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


__author__ = "Naoya INADA <naoina@kuune.org>"

__all__ = [
]

import unittest

import _groonga

from pyroonga.exceptions import GroongaError
from pyroonga.groonga import Groonga
from pyroonga.tests import GroongaTestBase


class TestGroongaWithNotConnected(unittest.TestCase):
    def test___init__(self):
        # test with default encoding
        grn = Groonga()
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_UTF8)
        self.assertFalse(grn.connected)

        # test with all encodings
        grn = Groonga(encoding='utf-8')
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_UTF8)
        self.assertFalse(grn.connected)
        grn = Groonga(encoding='euc-jp')
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_EUC_JP)
        self.assertFalse(grn.connected)
        grn = Groonga(encoding='sjis')
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_SJIS)
        self.assertFalse(grn.connected)
        grn = Groonga(encoding='latin1')
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_LATIN1)
        self.assertFalse(grn.connected)
        grn = Groonga(encoding='koi8-r')
        self.assertEqual(grn._ctx.get_encoding(), _groonga.ENC_KOI8R)
        self.assertFalse(grn.connected)

    def test_connect_not_running_server(self):
        grn = Groonga()
        self.assertRaises(GroongaError, grn.connect, host='', port=0)


class TestGroonga(GroongaTestBase):
    def test_connect(self):
        grn = Groonga()
        grn.connect(host='localhost', port=10041)
        self.assertTrue(grn.connected)
        self.assertEqual(grn.host, 'localhost')
        self.assertEqual(grn.port, 10041)

    def test_query(self):
        # test with not connected
        grn = Groonga()
        self.assertRaises(GroongaError, grn.query, 'a')

        # test with invalid command
        grn = Groonga()
        grn.connect('localhost', 10041)
        self.assertRaises(GroongaError, grn.query, 'a')

        # test the query
        grn = Groonga()
        grn.connect('localhost', 10041)
        result = grn.query('table_list')
        self.assertEqual(result, '''[[["id","UInt32"],["name","ShortText"],\
["path","ShortText"],["flags","ShortText"],["domain","ShortText"],\
["range","ShortText"]]]''')


def main():
    unittest.main()

if __name__ == '__main__':
    main()
