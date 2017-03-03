#!/usr/bin/python

import moduleframework
import pickle
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print debug info")

parser.add_option("-p", "--print",
                  action="store_true", dest="printt", default=False,
                  help="print output of called method")
(options, args) = parser.parse_args()

helper = None
picklefile = '/var/tmp/module-data.pkl'
method = args[0] if len(args)>0 else "close"

MODULE = moduleframework.MODULE if moduleframework.MODULE else "docker"

if options.verbose:
    print "called ", method, args[1:]

if os.path.isfile(picklefile) and os.stat(picklefile).st_size > 100:
    if options.verbose:
        print "reading from pickfile", picklefile
    pkl_file = open(picklefile, 'rb')
    if options.verbose:
        print "descriptor ", pkl_file
    helper = pickle.load(pkl_file)
    if options.verbose:
        print "reading from pickled object", helper
    pkl_file.close()
else:
    helper=moduleframework.get_correct_backend()
    if options.verbose:
        print "created new instance for module"

pkl_file = open(picklefile, 'wb')

if "close" != method:
    if method == "init":
        helper.setUp()
    elif method == "start":
        helper.start()
    elif method == "stop":
        helper.stop()
    else:
        if options.printt:
            if len(args)==1:
                print getattr(helper,method)()
            else:
                print getattr(helper,method)(" ".join(args[1:]))
        else:
            if len(args)==1:
                getattr(helper,method)()
            else:
                getattr(helper,method)(" ".join(args[1:]))
    pickle.dump(helper, pkl_file)

pkl_file.close()

if method == "close":
    helper.stop()
    os.remove(picklefile) if os.path.exists(picklefile) else None


