import argparse
import os
import re

argument_re=re.compile(r".*add_argument")

line_sep="\n"
indent="\t"

def load_file(file_path):
    with open(os.path.abspath(file_path),"r") as f:
        text=f.read()
    return text

def extract_args(text):

    def get_arg(text,start):
        assert text[start]=="(","First Char: {}".format(text[start])
        i=start
        net=1
        while net!=0:
            i+=1
            if text[i]=="(":
                net+=1
            if text[i]==")":
                net-=1

        arg= text[start:i + 1]
        arg=arg.replace("\n","")
        return arg

    args=[]
    for m in argument_re.finditer(text):
        start = m.span()[-1]
        args.append(get_arg(text, start))
    return args

def extract_dcts(text):

    args=extract_args(text)

    parser=argparse.ArgumentParser()
    for arg in args:
        eval("parser.add_argument{}".format(arg))

    help_dct={}
    default_dct={}
    type_dct={}

    dcts=help_dct,default_dct,type_dct

    for action in parser._actions:
        help_dct[action.dest]=action.help
        default_dct[action.dest]=action.default if action.default!= '==SUPPRESS==' else None
        if type(action)==argparse._StoreTrueAction or type(action) == argparse._StoreFalseAction:
            type_dct[action.dest]=bool
        else:
            type_dct[action.dest]=action.type

    for dct in dcts:
        if 'help' in dct: del dct['help']

    return dcts

def build_arg_list(default_dct):
    arg_list = []
    for arg, default in default_dct.items():
        if default is not None:
            arg_list.append("{}={}".format(arg,default))
        else:
            arg_list.append(arg)
    arg_list.sort(key=lambda arg_token: not "=" in arg_token)
    return arg_list

def build_signature(arg_list):
    args=",".join(arg_list)
    return "def main("+args+")"


def build_params_types(help_dct, type_dct):
    params = []
    types = []

    for arg in help_dct.keys():
        h, t = help_dct[arg], type_dct[arg]
        params.append(':param {}: {}'.format(arg, h))
        types.append(':type {}: {} [insert type description]'.format(arg, t))

    return params, types


def build_docstring(params, types):
    sep = line_sep + indent

    params=sep.join(params)
    types= sep.join(types)

    return sep.join(['"""',params,types,'"""'])


def build_get_args(text):
    sep = line_sep + indent
    spoofing_code = """a"""  # TODO

    dcts= help_dct, default_dct, type_dct=extract_dcts(text)

    arg_list = build_arg_list(default_dct)
    params, types = build_params_types(help_dct, type_dct)

    def key(arg):
        for index, a in enumerate(arg_list):
            if arg in a:
                return index

    params.sort(key=key)
    types.sort(key=key)

    get_args_string = sep.join([build_signature(arg_list), build_docstring(params, types), spoofing_code])
    print get_args_string
    return get_args_string

def main(file_path):
    text=load_file(file_path)
    get_args_string = build_get_args(text)

if __name__ == '__main__':
    main("./test_input.py")
