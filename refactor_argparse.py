import argparse,re

argument_re=re.compile(r".*add_argument")

parser = argparse.ArgumentParser()
parser.add_argument('--foo', default="hello", help='foo help')
parser.add_argument('bar', action="store_true", help='bar help')

def extract_args(file_path):

    def get_arg(text,start):
        assert(text[start]=="(")
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

    with open(file_path,"r") as f:
        text=f.read()
        for m in argument_re.finditer(text):
            start=m.span()[-1]+1
            args.append(get_arg(text,start))

    return args


def extract_dcts(file_path):

    parser=argparse.ArgumentParser()
    parser.add_argument()