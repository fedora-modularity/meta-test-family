from common import get_helpmd_file, print_info




class HelpMDLinter(object):
    """
    Class checks a Help.md file

    It requires only directory with help.md file.
    """

    help_md = None

    def __init__(self):
        help_md_file = get_helpmd_file()
        if help_md_file:
            with open(help_md_file, 'r') as f:
                lines = f.readlines()
                # Count with all lines which begins with #
                self.help_md = [x.strip() for x in lines if x.startswith('#')]
                # Count with all lines which begins with %
                self.help_md.extend([x.strip() for x in lines if x.startswith('%')])


    def get_image_name(self, name):
        name = '%% %s' % name
        if not self.help_md:
            return False
        tag_exists = [x for x in self.help_md if name.upper() in x]
        return tag_exists

    def get_maintainer_name(self, name):
        name = '%% %s' % name
        if not self.help_md:
            return False
        tag_exists = [x for x in self.help_md if name.startswith(x)]
        return tag_exists

    def get_tag(self, name):
        name = '# %s' % name
        tag_found = True
        if not self.help_md:
            print_info("help md does not exist.")
            return False
        if not [x for x in self.help_md if name.upper() in x]:
            tag_found = False
        return tag_found
