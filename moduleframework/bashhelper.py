#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Jan Scotka <jscotka@redhat.com>
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Jan Scotka <jscotka@redhat.com>
#

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
