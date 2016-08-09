import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pairs', type=str, default="./pairs.txt",
                        help='Location of the LFW pairs file from http://vis-www.cs.umass.edu/lfw/pairs.txt')
    parser.add_argument('--lfw-align', type=str, default="./lfw-align",
                        help='The directory of lfw-align, which contains the aligned lfw images')
    parser.add_argument('--suffix', type=str, default="png",
                        help='The type of image')
    parser.add_argument('--size', type=int, default=128,
                        help='the image size of lfw aligned image, only support squre size')
    parser.add_argument('--model-prefix', default='../model/lightened_cnn/lightened_cnn',
                        help='The trained model to get feature')
    parser.add_argument('--epoch', type=int, default=165,
                        help='The epoch number of model')
    parser.add_argument('--predict-file', type=str, default='./predict.txt',
                        help='The file which contains similarity distance of every pair image given in pairs.txt')
    parser.add_argument('bar', action="store_true", help='bar help')
    args = parser.parse_args()

if __name__ == '__main__':
    main()