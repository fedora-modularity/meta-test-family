from avocado import Test


class Add1(Test):
    """
    :avocado: enable
    :avocado: tags=add
    """

    def test(self):
        pass


class Add2(Test):
    """
    :avocado: enable
    """

    def test(self):
        """
        :avocado: tags=add
        """
        pass


class Add3(Test):
    """
    :avocado: enable
    """

    def test(self):
        pass
