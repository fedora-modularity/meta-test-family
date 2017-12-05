from avocado import Test


class Add1(Test):
    """
    :avocado: enable
    :avocado: tags=add
    """

    def test(self):
        pass


class AddPart(Test):
    """
    :avocado: enable
    :avocado: tags=add
    """

    def testAdd(self):
        pass

    def testBad(self):
        """
        :avocado: tags=rem
        """
        pass


class Rem2(Test):
    """
    :avocado: enable
    :avocado: tags=rem
    """

    def test(self):
        pass
