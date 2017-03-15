#!/usr/bin/python

import os
import pickle
import inspect
from moduleframework import module_framework
from optparse import OptionParser


def main():
    picklefile = '/var/tmp/module-data.pkl'
    parser = OptionParser()
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print debug info")
    parser.add_option("-p", "--print",
                      action="store_true", dest="printt", default=False,
                      help="print output of called method")
    (options, args) = parser.parse_args()

    if len(args) == 0:
        raise ValueError("Unable to call bash helper without function, there is possible to use: ", [ a[0] for a in inspect.getmembers(moduleframework.get_correct_backend(), predicate=inspect.ismethod) if '__' not in a[0] ])
    method = args[0]

    def printIfVerbose(*sargs):
        if options.verbose:
            print sargs

    if os.path.isfile(picklefile) and os.stat(picklefile).st_size > 100:
        printIfVerbose("reading from pickfile", picklefile)
        pkl_file = open(picklefile, 'rb')
        helper = pickle.load(pkl_file)
        printIfVerbose("reading from pickled object", helper)
        pkl_file.close()
    else:
        (helper, moduletype) = module_framework.get_correct_backend()
        printIfVerbose("created new instance for module")

    pkl_file = open(picklefile, 'wb')

    if "tearDown" != method:
        if options.printt:
            if len(args) == 1:
                print getattr(helper, method)()
            else:
                print getattr(helper, method)(" ".join(args[1:]))
        else:
            if len(args) == 1:
                getattr(helper, method)()
            else:
                getattr(helper, method)(" ".join(args[1:]))
        pickle.dump(helper, pkl_file)
        pkl_file.close()
    else:
        pkl_file.close()
        helper.tearDown()
        os.remove(picklefile) if os.path.exists(picklefile) else None


if __name__ == "__main__":
    main()
