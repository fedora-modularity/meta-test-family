
"""
Create agregation report (wiki style)

"""

import argparse
import common
import os


def get_options():
    parser = argparse.ArgumentParser(description='Create Coverage reports')
    parser.add_argument('-a', dest='action', default="statistic",
                        help='print to stdout in selected format (statistic - get covered percentage, md - get wiki format as MD file)')
    args = parser.parse_args()
    return args


def print_md_file(meta):
    items = meta.get_coverage()
    output = ["# Coverage for: %s" % os.path.basename(os.getcwd()), ""]
    output += ["## Description", meta.base_element.get(common.DESC) or "Not given", "", ""]
    output += ["## Tests"]
    for key in sorted(items):
        if items[key].get(common.SOURCE):
            output += ["* %s" % key]
            output += ["  * by: %s" % items[key].get(common.SOURCE)]
            output += ["  * description: %s" % items[key].get(common.DESC)]

        else:
            output += ["* %s (MISSING coverage)" % key]
            output += ["  * description: %s" % items[key].get(common.DESC)]
    output += ["", "## Overall Coverage: %s" % statistic(meta)]
    return output


def statistic(meta):
    items = meta.get_coverage()
    counter = 0
    all = len(items)
    for key, value in items.iteritems():
        if value.get(common.SOURCE):
            counter += 1
    return "%s%%" % (counter * 100 / all)


def main():
    options = get_options()
    meta = common.MetadataLoader()
    if options.action == "statistic":
        print statistic(meta)
    elif options.action == "md":
        print "\n".join(print_md_file(meta))
