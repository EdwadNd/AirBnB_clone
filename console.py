#!/usr/bin/python3
""" console shell """
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review



class HBNBCommand(cmd.Cmd):
    """ commandline interpreter forr HBNB """
    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {'BaseModel': BaseModel,'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
               }

    def do_quit(self, command):
        """Quit command to exit the program"""
        exit()

    def do_EOF(self, line):
        """ EOF command to exit the program"""
        return True

    def do_create(self, argument):
        """ command creates  new instance of classes """
        if not argument:
            print("** class name missing **")
            return
        elif argument not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        _instance = HBNBCommand.classes[argument]()
        storage.save()
        print(_instance.id)
        storage.save()

    def do_show(self, argument):
        """ Method to show an individual object """
        new = argument.partition(" ")
        obj_name = new[0]
        obj_Id = new[2]

        if obj_Id and ' ' in obj_Id:
            obj_Id = obj_Id.partition(' ')[0]

        if not obj_name:
            print("** class name missing **")
            return

        if obj_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not obj_Id:
            print("** instance id missing **")
            return

        key = obj_name + "." + obj_Id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")
    
    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        obj_name = new[0]
        obj_id = new[2]
        if obj_id and ' ' in obj_id:
            obj_id = obj_id.partition(' ')[0]

        if not obj_name:
            print("** class name missing **")
            return

        if obj_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not obj_id:
            print("** instance id missing **")
            return

        key = obj_name + "." + obj_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")
    
    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)
    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] is '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] is not ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] is '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file





if __name__ == '__main__':
    HBNBCommand().cmdloop()