import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bar', action="store_true", help='bar help')
    parser.add_argument("--foo", type=bool, help="foo help")
    args = parser.parse_args()

if __name__ == '__main__':
    main()