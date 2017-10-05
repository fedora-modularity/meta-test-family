from __future__ import print_function

import os
from moduleframework import common

HELP_MD = "help.md"


def get_help_md_file(dir_name):
    helpmd_file = os.path.join(os.path.abspath(dir_name), "help", HELP_MD)
    if not os.path.exists(helpmd_file):
        helpmd_file = None
        common.print_debug("help.md should exists in the %s directory." % dir_name)
    return helpmd_file


class HelpMDLinter(object):
    """
    Class checks a Help.md file

    It requires only directory with help.md file.
    """

    help_md = None

    def __init__(self, dir_name="../"):
        help_md_file = get_help_md_file(dir_name)
        if help_md_file:
            with open(help_md_file, 'r') as f:
                lines = f.readlines()
                # Count with all lines which begins with #
                self.help_md = [x.strip() for x in lines if x.startswith('#')]
                # Count with all lines which begins with %
                self.help_md.extend([x.strip() for x in lines if x.startswith('%')])
        else:
            self.help_md = None

    def get_image_maintainer_name(self, name):
        name = '% %s' % name
        if name.upper() in self.help_md:
            return True
        else:
            return False

    def get_tag(self, name):
        name = '# %s' % name
        if name.upper() in self.help_md:
            return True
        else:
            return False
