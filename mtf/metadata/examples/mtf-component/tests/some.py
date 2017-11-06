from mtf.metatest import AvocadoTest

class Add1(AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=add
    """
    def setUp(self):
        pass
    def tearDown(self, *args, **kwargs):
        pass
    def test(self):
        pass

class AddPart(AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=add
    """
    def setUp(self):
        pass
    def tearDown(self, *args, **kwargs):
        pass

    def test(self):
        pass

    def testBad(self):
        """
        :avocado: tags = rem
        """
        pass

class Rem2(AvocadoTest):
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
