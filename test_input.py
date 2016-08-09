import argparse

def main():
    print args.foo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', default="hello", help='foo help')
    parser.add_argument('bar', action="store_true", help='bar help')
    args=parser.parse_args()
    main()