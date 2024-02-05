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


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

class TestStorageGet(unittest.TestCase):
    """Testing get method in DBStorage"""

    def setUp(self):
        """setUp method"""
        self.state = State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """testing get method"""
        result = models.storage.get(cls="State", id=self.state.id)

        self.assertIsInstance(result, State)

    def test_get_method_return(self):
        """Testing get method for id match"""
        result = models.storage.get(cls="State", id=str(self.state.id))

        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """Testing get method for None return value"""
        result = models.storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(result)


@unittest.skipIf(models.storage_type != 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """Tests the count method in DBStorage"""

    def setup(self):
        """setup method"""
        self.state1 = State(name="Kitui")
        self.state1.save()
        self.state2 = State(name="Kisii")
        self.state2.save()
        self.state3 = State(name="Machakos")
        self.state3.save()
        self.state4 = State(name="Virgina")
        self.state4.save()
        self.state5 = State(name="Qatar")
        self.state5.save()
        self.state6 = State(name="Kampi")
        self.state6.save()
        self.state7 = State(name="Kaptere")
        self.state7.save()

    def test_count_all(self):
        """Testing counting all instances"""
        result = models.storage.count()

        self.assertEqual(len(models.storage.all()), result)

    def test_count_state(self):
        """Testing counting state instances"""
        result = models.storage.count(cls="State")

        self.assertEqual(len(models.storage.all("State")), result)

    def test_count_city(self):
        """Testing counting non-existent"""
        result = models.storage.count(cls="City")

        self.assertEqual(int(0 if len(models.storage.all("City")) is None else
                             len(models.storage.all("City"))), result)

if __name__ == '__main__':
    unittest.main
