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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
    except Exception as e:
        print("[!] Error: {0}".format(e))
        sys.exit(1)
    return 0


if __name__ == "__main__":
    main()
