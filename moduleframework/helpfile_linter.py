from __future__ import print_function

import os
from moduleframework import common

HELP_MD = "help.md"


class HelpMDLinter(object):
    """
    Class checks a Help.md file

    It requires only directory with help.md file.
    """

    help_md = None

    def __init__(self, dockerfile=None):
        if dockerfile is None:
            dir_name = os.getcwd()
        else:
            dir_name = os.path.dirname(dockerfile)
        help_md_file = os.path.join(dir_name, HELP_MD)
        common.print_debug("help.md path is %s." % help_md_file)
        if os.path.exists(help_md_file):
            with open(help_md_file, 'r') as f:
                lines = f.readlines()
                # Count with all lines which begins with #
                self.help_md = [x.strip() for x in lines if x.startswith('#')]
                # Count with all lines which begins with %
                self.help_md.extend([x.strip() for x in lines if x.startswith('%')])
        else:
            common.print_debug("help.md should exists in the %s directory." % dir_name)
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
