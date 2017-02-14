#!/usr/bin/env python3.6

import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: {0} <FILE>.tar")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("[!] Error: File does not exists.")
        sys.exit(1)

    try:
        with tarfile.open(sys.argv[1], 'r:gz') as tar:
            tar.extractall()
    except Exception as e:
        print("[!] Error: {0}".format(e))
        sys.exit(1)
    return 0


if __name__ == "__main__":
    main()
