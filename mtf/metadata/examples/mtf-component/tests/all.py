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


class Add2(AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        pass
    def tearDown(self, *args, **kwargs):
        pass
    def test(self):
        """
        :avocado: tags = add
        """
        pass

class Add3(AvocadoTest):
    """
    :avocado: enable
    """
    def setUp(self):
        pass
    def tearDown(self, *args, **kwargs):
        pass
    def test(self):
        pass
