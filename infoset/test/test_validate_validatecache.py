#!/usr/bin/env python3
"""Test the ValidateCache class in the infoset.cache.validate module."""

# Standard imports
import unittest
import tempfile
import json
import copy
import os

# Infoset imports
from infoset.cache import validate
from infoset.test import unittest_db
from infoset.utils import general
from infoset.test import unittest_variables


class TestValidateCache(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = unittest_variables.TestVariables().cache_data()

    def test___init__(self):
        """Testing function __init__."""
        # Initialize key variables
        directory = tempfile.mkdtemp()
        id_agent = self.data['id_agent']
        last_timestamp = self.data['timestamp']
        filepath = ('%s/%s_%s_%s.json') % (
            directory,
            last_timestamp,
            id_agent,
            general.hashstring(general.randomstring()))

        # Drop the database and create tables
        unittest_db.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        self.assertEqual(result.valid(), True)

        # Test with invalid data (string)
        result = validate.ValidateCache(data='string')
        self.assertEqual(result.valid(), False)

        # Test with invalid data (string)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('agent', None)
        result = validate.ValidateCache(data=data_dict)
        self.assertEqual(result.valid(), False)

        # Write good data to file and test
        with open(filepath, 'w') as f_handle:
            json.dump(self.data, f_handle)
        result = validate.ValidateCache(filepath=filepath)
        self.assertEqual(result.valid(), True)

        #################################################################
        #################################################################
        # Add record to DeviceAgent table and test for validity with the
        # same data, which should be False
        #################################################################
        #################################################################

        unittest_db.setup_db_deviceagent(self.data)

        # Attempting to insert duplicate data should fail
        with open(filepath, 'w') as f_handle:
            json.dump(self.data, f_handle)
        result = validate.ValidateCache(filepath=filepath)
        self.assertEqual(result.valid(), False)

        #################################################################
        #################################################################
        # Test with invalid data in file
        #################################################################
        #################################################################

        # Drop the database and create tables
        unittest_db.initialize_db()

        # Write bad data to file and test
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('agent', None)
        with open(filepath, 'w') as f_handle:
            json.dump(data_dict, f_handle)
        result = validate.ValidateCache(filepath=filepath)
        self.assertEqual(result.valid(), False)

        # Cleanup
        os.remove(filepath)
        os.removedirs(directory)

    def test_getinfo(self):
        """Testing function getinfo."""
        # Drop the database and create tables
        unittest_db.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        data_dict = result.getinfo()

        # Check main keys
        for key, _ in self.data.items():
            self.assertEqual(self.data[key], data_dict[key])

    def test_valid(self):
        """Testing function valid."""
        # Drop the database and create tables
        unittest_db.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        self.assertEqual(result.valid(), True)

        # Test with invalid data (string)
        result = validate.ValidateCache(data='string')
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
