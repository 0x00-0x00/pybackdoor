#!/usr/bin/env python3.6
import tarfile
import os


# Static variables
INSTALL_FOLDER = os.environ["ALLUSERSPROFILE"]
FOLDER_NAME = "a22f53c72d82e19a7dc3fff940f35b62"
INSTALL_FOLDER + os.sep + FOLDER_NAME
SOURCE_FILE = "compress.tar"


def folder_set_up():
    """
    Create the destination folder to receive extracted data.
    """
    try:
        if not os.path.exists(INSTALL_FOLDER):
            os.mkdir(INSTALL_FOLDER)
        return 0
    except Exception as e:
        print("[!] Error: {0}".format(e))
        return -1


def decompress(source):
    """
    Decompress the file into the install folder.
    """
    try:
        with tarfile.open(source, 'r:gz') as tar:
            tar.extractall(path=INSTALL_FOLDER)
    except Exception as e:
        print("[!] Error: {0}".format(e))
        return -1
    return 0


def main():
    #  Create the folder
    if not folder_set_up():
        return -1

    #  Decompress the data
    if not decompress(SOURCE_FILE):
        return -1

    return 0


if __name__ == "__main__":
    main()

