from avocado import Test


class Rem1(Test):
    """
    :avocado: enable
    :avocado: tags=rem
    """

    def test(self):
        pass


class Rem2(Test):
    """
    :avocado: enable
    """

    def test(self):
        """
        :avocado: tags=rem
        """
        pass


class Rem3(Test):
    """
    :avocado: disable
    """

    def test(self):
        pass
