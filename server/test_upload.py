#
# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Author: Frederic Lepied <frederic.lepied@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import upload


class TestUpload(unittest.TestCase):

    def test_is_included_same(self):
        a = {'a': 1}
        self.assert_(upload.is_included(a, a))

    def test_is_included_different(self):
        a = {'a': 1}
        b = {'a': 2}
        self.assert_(not upload.is_included(a, b))

    def test_is_included_more(self):
        a = {'a': 1, 'b': 2}
        b = {'a': 1, 'b': 2, 'c': 3}
        self.assert_(upload.is_included(a, b))

    def test_generate_ips(self):
        model = '192.168.1.10-12'
        self.assertEqual(list(upload._generate_values(model)),
                         ['192.168.1.10',
                          '192.168.1.11',
                          '192.168.1.12'])

    def test_generate_names(self):
        model = 'host10-12'
        self.assertEqual(list(upload._generate_values(model)),
                         ['host10', 'host11', 'host12'])

    def test_generate_nothing(self):
        model = 'host'
        result = upload._generate_values(model)
        self.assertEqual(result.next(),
                         'host')

    def test_generate_range(self):
        self.assertEqual(list(upload._generate_range('10-12')),
                         ['10', '11', '12'])

    def test_generate_range_colon(self):
        self.assertEqual(list(upload._generate_range('1-3:10-12')),
                         ['1', '2', '3', '10', '11', '12'])

    def test_generate(self):
        model = {'gw': '192.168.1.1',
                 'ip': '192.168.1.10-12',
                 'hostname': 'host10-12'}
        self.assertEqual(
            upload.generate(model),
            [{'gw': '192.168.1.1', 'ip': '192.168.1.10', 'hostname': 'host10'},
             {'gw': '192.168.1.1', 'ip': '192.168.1.11', 'hostname': 'host11'},
             {'gw': '192.168.1.1', 'ip': '192.168.1.12', 'hostname': 'host12'}]
            )

    def test_generate_253(self):
        result = upload.generate({'hostname': '10.0.1-2.2-254'})
        self.assertEqual(
            len(result),
            2 * 253,
            result)

    def test_generate_list(self):
        result = upload.generate({'hostname': ('hosta', 'hostb', 'hostc')})
        self.assertEqual(
            result,
            [{'hostname': 'hosta'},
             {'hostname': 'hostb'},
             {'hostname': 'hostc'}]
            )

    def test_generate_none(self):
        model = {'gateway': '10.66.6.1',
                 'ip': '10.66.6.100',
                 'netmask': '255.255.255.0',
                 'gateway-ipmi': '10.66.6.1',
                 'ip-ipmi': '10.66.6.110',
                 'netmask-ipmi': '255.255.255.0',
                 'hostname': 'hp-grid'
                 }
        result = upload.generate(model)
        self.assertEqual(result, [model])

    def test_update_cmdb_simple(self):
        cmdb = [{}]
        var = {'a': 1}
        result = upload.update_cmdb(cmdb, var, var, False)
        self.assertTrue(result, cmdb)

    def test_update_cmdb_reuse(self):
        cmdb = [{'a': 1, 'used': 1}]
        var = {'a': 1}
        result = upload.update_cmdb(cmdb, var, var, False)
        self.assertTrue(result, cmdb)

    def test_update_cmdb_full(self):
        cmdb = [{'a': 2, 'used': 1}]
        var = {'a': 1}
        result = upload.update_cmdb(cmdb, var, var, False)
        self.assertFalse(result, cmdb)

    def test_update_cmdb_full2(self):
        cmdb = [{'a': 'ff:ff'}]
        var = {'a': 'FF:FF'}
        result = upload.update_cmdb(cmdb, var, var, True)
        self.assertFalse(result, cmdb)

if __name__ == "__main__":
    unittest.main()
