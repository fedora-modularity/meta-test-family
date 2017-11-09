from mtf.metatest import AvocadoTest


class Rem1(AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=rem
    """

    def setUp(self):
        pass

    def tearDown(self, *args, **kwargs):
        pass

    def test(self):
        pass


class Rem2(AvocadoTest):
    """
    :avocado: enable
    """

    def setUp(self):
        pass

    def tearDown(self, *args, **kwargs):
        pass

    def test(self):
        """
        :avocado: tags=rem
        """
        pass


class Rem3(AvocadoTest):
    """
    :avocado: disable
    """

    def setUp(self):
        pass

    def tearDown(self, *args, **kwargs):
        pass

    def test(self):
        pass
