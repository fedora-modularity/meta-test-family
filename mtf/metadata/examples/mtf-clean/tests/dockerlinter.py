from avocado import Test


class DockerFileLint(Test):
    """
    :avocado: enable
    :avocado: tags=dockerfilelint,docker,rhel,fedora
    """

    def test(self):
        pass


class DockerLint(Test):
    """
    :avocado: enable
    :avocado: tags=dockerlint,docker,rhel,fedora
    """

    def test(self):
        pass
