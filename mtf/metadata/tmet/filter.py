import argparse
import common
import re

def get_options():
    parser = argparse.ArgumentParser(description='Filter and print tests')
    parser.add_argument('-r', dest='relevancy', default='',
                        help='apply relevancy filtering, expect environment specification')
    parser.add_argument('-t', dest='tags', default='',
                        help='apply tags filtering, expect tags in DNF form')
    args = parser.parse_args()
    return args

def filter_avocado_tags(tags_input,tags_filters):
    pass

def filters(meta, relevancy, tags):
    items = meta.get_coverage()
    output = []
    for key in sorted(items):
        value = items[key]
        #### APPLY FILTERS ######
        source = value.get(common.SOURCE) or ""
        if re.match(r".*://.*", source):
            output.append(source)
        elif re.match(r".*", source):
            output.append('file://%s/%s' % (key, source))

    return output

def main():
    options = get_options()
    meta = common.MetadataLoader()
    print " ".join(filters(meta, options.relevancy, options.tags))
