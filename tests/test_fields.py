import unittest
import os

import cnfrm

test_dir = os.path.dirname(os.path.abspath(__file__))

class TestFields(unittest.TestCase):
    class Config(cnfrm.Config):
        email = cnfrm.EmailField()
        name = cnfrm.Field()
        age = cnfrm.IntegerField(min_value=0)
        size = cnfrm.FloatField(max_value=2.2)
        path = cnfrm.FileField(required=False)
        directory = cnfrm.DirectoryField(required=False)
        url = cnfrm.UrlField()

    def setUp(self):
        self.config = self.Config().read_dct(self.get_dct())

    @staticmethod
    def get_dct():
        return {
            "email": "me@you.com",
            "name": "Donald Duck",
            "age": 20,
            "size": 1.2,

        }
    
    def assertRaisesValidation(self):
        return self.assertRaises(ValueError)

    def test_field_values(self):
        for key, value in self.get_dct().items():
            self.assertEqual(getattr(self.config, key), value)

    def test_email(self):
        with self.assertRaisesValidation():
            self.config.email = "me@you"

    def test_int(self):
        with self.assertRaisesValidation():
            self.config.age = 20.2
        
        with self.assertRaisesValidation():
            self.config.age = -3
        

    def test_float(self):
        with self.assertRaisesValidation():
            self.config.size = "nooo"
        

        with self.assertRaisesValidation():
            self.config.size = 7.
        
        # set an integer
        self.config.size = 1
    
    def test_directory(self):
        self.config.directory = test_dir

        with self.assertRaisesValidation():
            self.config.directory = os.path.join(test_dir, "test_fields.py")

    def test_file(self):
        self.config.path = os.path.join(test_dir, "test_fields.py")

        with self.assertRaisesValidation():
            self.config.path = test_dir
    
<<<<<<< HEAD
    def test_dump(self):
=======
    def test_write_json(self):
>>>>>>> 94e03d9 (update readme, rename dump_json function)
        self.config.write_json("test.json")
        config2 = self.Config().read_json("test.json")

        for key in self.config.get_fieldnames():
            self.assertEqual(getattr(self.config, key), getattr(config2, key))




if __name__ == '__main__':
    unittest.main()