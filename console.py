#!/usr/bin/python3
""" console shell """
import cmd
import sys
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ commandline interpreter forr HBNB """
    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {'BaseModel': BaseModel}

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



if __name__ == '__main__':
    HBNBCommand().cmdloop()