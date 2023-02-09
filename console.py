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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
