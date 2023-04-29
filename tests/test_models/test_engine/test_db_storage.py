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
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = DBStorage()
        storage.reload()
        all_objs = storage.all()
        lent = len(all_objs)
        Amenity.save(Amenity(name="test"))
        all_objs = storage.all()
        self.assertEqual(len(all_objs), lent + 1)
        self.assertIn('Amenity.test', all_objs)
        storage.delete(all_objs['Amenity.test'])
        storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        # storage = DBStorage()
        # storage.reload()
        # obj = State(name="test")
        # storage.new(obj)
        # key = obj.__class__.__name__ + '.' + obj.id
        # self.assertIn(key, storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test the save method of DBStorage"""
        # storage = DBStorage()
        # new_state = State()
        # new_state.name = "California"
        # storage.new(new_state)
        # storage.save()
        # all_states = storage.all(State)
        # self.assertIn(new_state, all_states.values())

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves an object from DBStorage"""
        storage = DBStorage()
        new_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                new_dict[instance_key] = instance
                storage._DBStorage__session = new_dict
                retrieved = storage.get(value, instance.id)
                self.assertEqual(retrieved, instance)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the number of objects in storage"""
        storage = DBStorage()
        new_dict = {}
        count = 0
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                new_dict[instance_key] = instance
                count += 1
                storage._DBStorage__session = new_dict
                self.assertEqual(storage.count(), count)
