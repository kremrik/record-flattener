from flattener.flattener import flatten, _flatten_list
import unittest
from unittest import skip


class test_flatten(unittest.TestCase):

    def test_wrong_args_1(self):
        record = {}
        with self.assertRaises(AssertionError):
            flatten(record=record, parse_lists=True)

    def test_wrong_args_2(self):
        record = {}
        with self.assertRaises(AssertionError):
            flatten(record=record, list_key_id="id")

    def test_wrong_args_3(self):
        record = {}
        with self.assertRaises(AssertionError):
            flatten(record=record, full_list_flatten=True)

    def test_wrong_args_4(self):
        record = {}
        with self.assertRaises(AssertionError):
            flatten(record=record, parse_lists=True, full_list_flatten=True)

    def test_wrong_args_5(self):
        record = {}
        with self.assertRaises(AssertionError):
            flatten(record=record, list_key_id="id", full_list_flatten=True)

    def test_null_case(self):
        record = {}
        gold = {}
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_base_case(self):
        record = {"key": "value"}
        gold = {"key": "value"}
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_mult_base_keys(self):
        record = {
            "key1": "value1",
            "key2": "value2"
            }
        gold = {
            "key1": "value1",
            "key2": "value2"
            }
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_simple_nest(self):
        record = {
            "k1": {
                "k2": 1
            }
        }
        gold = {
            "k1.k2": 1
        }
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_mix_levels(self):
        record = {
            "k1": {
                "k2": 1
            },
            "k1_2": "hi"
        }
        gold = {
            "k1.k2": 1,
            "k1_2": "hi"
        }
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_array_of_primitives(self):
        record = {
            "key": [1, 2]
        }
        gold = {
            "key": [1, 2]
        }
        output = flatten(record)
        self.assertEqual(gold, output)

    def test_no_array_flattening(self):
        record = {
            "key": [
                {"k": "v"}
            ]
        }
        gold = {
            "key": [
                {"k": "v"}
            ]
        }
        output = flatten(record, parse_lists=False)
        self.assertEqual(gold, output)

    def test_flatten_null_array(self):
        record = {
            "key": []
        }
        gold = {
            "key": []
        }
        output = flatten(record, parse_lists=True, list_key_id="id", full_list_flatten=True)
        self.assertEqual(gold, output)

    def test_partial_array_flatten(self):
        record = {
            "person": {
                "name": {
                    "first": "Joe",
                    "last": "Smith"
                },
                "address": "123 Place Ave"
            },
            "phone_numbers": [
                {
                    "type": "cell",
                    "number": 1112223333
                },
                {
                    "type": "home",
                    "number": 4445556666
                }
            ]
        }

        gold = {
            "person.name.first": "Joe",
            "person.name.last": "Smith",
            "person.address": "123 Place Ave",
            "phone_numbers": {
                "cell": {
                    "number": 1112223333
                },
                "home": {
                    "number": 4445556666
                }
            }
        }

        output = flatten(record, parse_lists=True, list_key_id="type", full_list_flatten=False)
        self.assertEqual(gold, output)

    def test_full_array_flatten(self):
        record = {
            "person": {
                "name": {
                    "first": "Joe",
                    "last": "Smith"
                },
                "address": "123 Place Ave"
            },
            "phone_numbers": [
                {
                    "type": "cell",
                    "number": 1112223333
                },
                {
                    "type": "home",
                    "number": 4445556666
                }
            ]
        }

        gold = {
            "person.name.first": "Joe",
            "person.name.last": "Smith",
            "person.address": "123 Place Ave",
            "phone_numbers.cell.number": 1112223333,
            "phone_numbers.home.number": 4445556666
        }

        output = flatten(record, parse_lists=True, list_key_id="type", full_list_flatten=True)
        self.assertEqual(gold, output)


class test_flatten_list(unittest.TestCase):

    def test_null_case(self):
        records = []
        list_key_id = None

        gold = []
        output = _flatten_list(records, list_key_id)
        self.assertEqual(gold, output)

    def test_list_of_primitives(self):
        records = [1, 2]
        list_key_id = None

        gold = [1, 2]
        output = _flatten_list(records, list_key_id)
        self.assertEqual(gold, output)

    def test_list_of_dicts(self):
        records = [
            {
                "id": "ID",
                "value": "value"
            }
        ]
        list_key_id = "id"

        gold = {
            "ID": {
                "value": "value"
            }
        }
        output = _flatten_list(records, list_key_id)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
