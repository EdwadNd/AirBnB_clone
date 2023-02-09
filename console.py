#!/usr/bin/python3
""" console shell """
import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """ comandline processor """
    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    def do_quit(self, command):
        """Quit command to exit the program"""
        exit()

    def do_EOF(self, line):
        """ Method to exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
