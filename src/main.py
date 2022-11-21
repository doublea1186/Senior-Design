# from utility import transcribe
import argparse
import sys

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="A script for Question Answer Generation")
    parser.add_argument("path")
    parser.add_argument('test')
    args = parser.parse_args()

    print(args.path)
    print(args.test)