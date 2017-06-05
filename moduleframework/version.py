#!/usr/bin/python

import os

SPECFILEPATH = os.path.abspath(
    # Path to SPECFILE
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "distro",
        "modularity-testing-framework.spec"
    ))


def version_func():
    with open(SPECFILEPATH, 'r') as infile:
        for line in infile.readlines():
            if "Version:        " in line:
                return line[16:].strip()
    raise BaseException(
        "Unable to read Version string from specfile:", SPECFILEPATH)


VERSION = version_func()

if __name__ == '__main__':
    print VERSION
