#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        test_args = {'updated_at': datetime(2024, 4, 2, 00, 31, 54, 233674),
                    'id': "0324",
                    'created_at': datetime(2024, 4, 2, 00, 31, 54, 233000),
                    'name': 'wifi'}
        cls.model = Amenity(**test_args)


    def tearDownClass(cls):
        storage.close()

    def test_all(self):
        l1 = len(storage.all('State'))
        state = State(name="State test all")
        state.save()
        output = storage.all('State')
        self.assertEqual(len(output), l1 + 1)
        self.assertIn(state.id, output.keys())


    def test_new(self):
        """test that new adds an object to the database"""
        test_len = len(storage.all())
        self.model.save()
        self.assertEqual(len(storage.all())), test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.assertEqual(len(storage.all())), test_len + 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        test_len = len(storage.all())
        a = Amenity(name="another")
        a.save()
        self.assertEqual(len(storage.all())), test_len + 1)
        b = State(name="California")
        self.assertNotEqual(len(storage.all())), test_len + 2)
        b.save()
        self,assertEqual(len(storage.all())), test_len + 2)


    def test_delete(self):
        all_storage = storage.all()
        test_len = len(all_storage)
        for v in all_storage.values():
            storage.delete(v)
            test_len -= 1
            self.assertGreaterEqual(test_len, storage.count())

    def test_reload(self):
        """not actually testing reload as it creates a parallel new session"""
        a = Amenity(name="different")
        a.save()
        for value in storage.all().values():
            self.assertIsInstance(value.created_at, datetime)    

    def test_state(self):
        """test State creation with a keyword argument"""
        a = State(name="Fabulous", id="HopeFab99")
        a.save()
        self.assertIn("HopeFab99", storage.all("State").keys())


    def test_count(self):
        """test count all"""
        test_len = len(storage.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.assertEqual(test_len + 1, storage.count())
        b = State(name="State test count")
        b.save()
        self.assertEqual(test_len + 2, storage.count())
        storage.delete(b)
        self.assertEqual(test_len + 1, storage.count())


    def test_count_amenity(self):
        """test_count with an argument"""
        test_len = len(storage.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.assertEqual(test_len + 1, storage.count("Amenity"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("Amenity"))

    def test_count_state(self):
        """test count with an Argument"""
        test_len = len(storage.all("State"))
        a = State(name="test_state_count_arg")
        a.save()
        self.assertEqual(test_len + 1, storage.count("State"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("State"))

    def test_count_bad_arg(self):
        """test with fake class name"""
        self.assertEqual(-1, storage.count("Fake"))

    def test_get_amenity(self):
        """test get with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        result = storage.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)

        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("Amenity", "test_3")
        self.assertIsNone(result)

    def test_get_state(self):
        """test get with valid cls and id"""
        a = State(name="test_state3", id="test_3")
        a.save()
        result = storage.get("State", "test_3")
        self.assertEqual(a.name, result.name)

        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("State", "test_3")
        self.assertIsNone(result)

    def test_get_bad_cls(self):
        """test get with invalid cls"""
        result = storage.get("Fake", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """test get with invalid id"""
        result = storage.get("State", "very_bad_id")

if __name__ == "__main__":
    import sys
    inport os
    sys.path.insert(1, os.path.join(os.path.spilt(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import Filestorage
    unittest.main()
