#!/usr/bin/env python3.6
import tarfile
import os
import argparse


def make_tarfile(output, source_dir):
    try:
        with tarfile.open(output, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return 0
    except Exception as e:
        print("[Error] {0}".format(e))
        return -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, type=str, help='Output file')
    parser.add_argument('-s', '--source', required=True, type=str, help='Source dir to compress')
    args = parser.parse_args()
    print("[+] Compressing {0}".format(args.source_dir))
    if make_tarfile(args.output, args.source) == 0:
        print("[+] Compression complete.")
    return 0


if __name__ == "__main__":
    main()
