#!/usr/bin/env python3

import unittest

from frontend import extend, Constructor


class TestExtend(unittest.TestCase):

    def test_extend_empty_empty(self):
        d3 = extend({}, {})
        self.assertEqual(d3, {'config': {}})

    def test_extend_empty_nonempty_no_config(self):
        d3 = extend({}, {'a': 1})
        self.assertEqual(d3, {'a': 1, 'config': {}})

    def test_extend_nonempty_nonempty_no_config(self):
        d3 = extend({'a': 1}, {'b': 2})
        self.assertEqual(d3, {'a': 1, 'b': 2, 'config': {}})

    def test_extend_config_not_dict(self):
        self.assertRaises(AttributeError, extend, {'a': 1}, {'config': 2})

    def test_extend_fresh_config(self):
        d3 = extend({'a': 1}, {'b': 2, 'config': {'c': 3}})
        self.assertEqual(d3, {'a': 1, 'b': 2, 'config': {'c': 3}})

    def test_extend_keep_config(self):
        d3 = extend({'a': 1, 'config': {'c': 3}}, {'b': 2})
        self.assertEqual(d3, {'a': 1, 'b': 2, 'config': {'c': 3}})

    def test_extend_change_config(self):
        d3 = extend({'a': 1, 'config': {'c': 3}}, {'b': 2, 'config': {'c': 4}})
        self.assertEqual(d3, {'a': 1, 'b': 2, 'config': {'c': 4}})

    def test_extend_extend_config(self):
        d3 = extend({'a': 1, 'config': {'c': 3}}, {'b': 2, 'config': {'d': 4}})
        self.assertEqual(d3, {'a': 1, 'b': 2, 'config': {'c': 3, 'd': 4}})


class TestConstructor(unittest.TestCase):

    def test_constructor_empty_empty(self):
        c = Constructor({})
        self.assertEqual(c.construct({}, {}), {'config': {}})

'''
    def test_constructor_02(self):
        c = Constructor({'extends': 'x'})
        self.assertEqual(c.construct({}, {'x': {'config': {'a'}}}), {'config': {}})
'''


if __name__ == '__main__':
    unittest.main()

