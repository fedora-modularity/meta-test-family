from __future__ import print_function

import os
from moduleframework import common

HELP_MD = "help.md"


def get_help_md_file(dockerfile):
    helpmd_file = os.path.join(os.path.dirname(dockerfile), HELP_MD)
    common.print_debug("help.md path is %s." % helpmd_file)
    if not os.path.exists(helpmd_file):
        helpmd_file = None
        common.print_debug("help.md should exists in the %s directory." % os.path.abspath(dockerfile))
    return helpmd_file


class HelpMDLinter(object):
    """
    Class checks a Help.md file

    It requires only directory with help.md file.
    """

    help_md = None

    def __init__(self, dockerfile=None):
        help_md_file = get_help_md_file(dockerfile)
        if help_md_file:
            with open(help_md_file, 'r') as f:
                lines = f.readlines()
                # Count with all lines which begins with #
                self.help_md = [x.strip() for x in lines if x.startswith('#')]
                # Count with all lines which begins with %
                self.help_md.extend([x.strip() for x in lines if x.startswith('%')])
        else:
            self.help_md = None

    def get_image_name(self, name):
        name = '%% %s' % name
        tag_exists = [x for x in self.help_md if name.upper() in x]
        return tag_exists

    def get_maintainer_name(self, name):
        name = '%% %s' % name
        tag_exists = [x for x in self.help_md if name.startswith(x)]
        return tag_exists

    def get_tag(self, name):
        name = '# %s' % name
        tag_exists = [x for x in self.help_md if name.upper() in x]
        return tag_exists
