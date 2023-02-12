#!/usr/bin/python3
""" module defines a class to manage storage"""
import json


class FileStorage:
    """This class serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """ all the objects in the file"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """saves  objects to json file"""
        with open(FileStorage.__file_path, 'w') as f:
            tmp = {}
            tmp.update(FileStorage.__objects)
            for key, val in tmp.items():
                tmp[key] = val.to_dict()
            json.dump(tmp, f)

    def reload(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        class_rep = {'BaseModel': BaseModel,'User': User}
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = class_rep[val['__class__']](**val)
        except FileNotFoundError:
            pass
