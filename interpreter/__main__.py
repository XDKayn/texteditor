import imp
import os
import sys
import tokenize
import argparse

# from interpreter.VirtualMachine import VirtualMachine
from VirtualMachine import VirtualMachine

try:
    open_source = tokenize.open
except:
    def open_source(fname):
        return open(fname, 'rU')

NoSource = Exception


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Python Interpreter")

    parser.add_argument('--filename', type=str, help='Input Python file')

    return parser.parse_args()


def exec_code_object(code, env):
    vm = VirtualMachine()
    vm.run_code(code, f_globals=env)


BUILTINS = sys.modules['builtins']


def rsplit1(s, sep):
    parts = s.split(sep)
    return sep.join(parts[:-1]), parts[-1]


def run_python_file(filename, args, package=None):
    old_main_mod = sys.modules['__main__']
    main_mod = imp.new_module('__main__')
    sys.modules['__main__'] = main_mod
    main_mod.__file__ = filename
    if package:
        main_mod.__package__ = package
    main_mod.__builtins__ = BUILTINS

    old_argv = sys.argv
    old_path0 = sys.path[0]
    sys.argv = args
    if package:
        sys.path[0] = ''
    else:
        sys.path[0] = os.path.abspath(os.path.dirname(filename))
    try:
        try:
            source_file = open_source(filename)
        except IOError:
            raise NoSource('No file to run: %r' % filename)

        try:
            source = source_file.read()
        finally:
            source_file.close()

        if not source or source[-1] != '\n':
            source += '\n'

        code_obj = compile(source, filename, 'exec')

        # print(code_obj)

        exec_code_object(code_obj, main_mod.__dict__)
    finally:
        sys.modules['__main__'] = old_main_mod

        sys.argv = old_argv
        sys.path[0] = old_path0


if __name__ == '__main__':
    args = parse_args()
    run_python_file(args.filename, None)
    # run_python_file('E:/alphaCoder/test/test1.py', None)
