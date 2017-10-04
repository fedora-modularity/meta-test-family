from __future__ import print_function

import mistune
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
            renderer = mistune.Renderer(escape=False,
                                        hard_wrap=False,
                                        parse_block_html=False,
                                        parse_inline_html=False)
            md = mistune.Markdown(renderer=renderer)
            with open(help_md_file, 'r') as f:
                self.help_md = md.parse(f.read())
        else:
            self.help_md = None
        print(self.help_md)

    def get_image_name(self):
        pass

    def get_maintainer(self):
        pass

    def get_date(self):
        pass

    def get_name(self):
        pass

    def get_description(self):
        pass

    def get_usage(self):
        pass

    def get_environment_variables(self):
        pass

    def get_labels(self):
        pass

    def get_security_implications(self):
        pass
