"""
Filter testcases based on various parameters

"""
import argparse
import common


def get_options():
    parser = argparse.ArgumentParser(description='Filter and print tests')
    parser.add_argument('-r', dest='relevancy',
                        help='apply relevancy filtering, expect environment specification')
    parser.add_argument(
        '-t',
        dest='tags',
        action="append",
        help='apply tags filtering, expect tags in DNF form (expressions in one option means AND, more -t means OR)')
    parser.add_argument('-b', dest='backend',
                        help='output for selected backend')
    parser.add_argument('--location', dest='location', default='.',
                        help='output for selected backend')
    parser.add_argument('--linters', dest='linters', action='store_true',
                        help='output for selected backend')
    parser.add_argument('--nofilters', dest='nofilters', action='store_true',
                        help='disable all filters in config file and show all tests for backend')
    parser.add_argument('tests', nargs='*', help='import tests for selected backed')

    args = parser.parse_args()
    return args


def main():
    options = get_options()
    output = filtertests(backend=options.backend,
                         location=options.location,
                         linters=options.linters,
                         tests=options.tests,
                         tags=options.tags,
                         relevancy=options.relevancy,
                         applyfilters=not options.nofilters
                         )
    print " ".join([x[common.SOURCE] for x in output])


def filtertests(backend, location, linters, tests, tags, relevancy, applyfilters=True):
    """
    Basic method to use it for wrapping inside another python code,
    allows apply tag filters and relevancy

    :param backend:
    :param location:
    :param linters:
    :param tests:
    :param tags:
    :param relevancy:
    :return:
    """
    meta = common.get_backend_class(backend)(location=location,
                                             linters=linters,
                                             backend=backend)
    if tests:
        for test in tests:
            meta._import_tests(test)

    if applyfilters:
        meta.add_filter(tags=tags, relevancy=relevancy)
        return meta.apply_filters()
    else:
        return meta.backend_tests()
