from moduleframework import module_framework


def test_simple():
    backend, moduletype = module_framework.get_backend()
    backend.setUp()
    backend.start()
    assert "bin" in backend.run("ls /").stdout
    backend.tearDown()

class TestExampleTwo:
    def setUp(self):
        self.backend, self.moduletype = module_framework.get_backend()
        self.backend.setUp()
        self.backend.start()

    def test_simpleinclass(self):
        assert "bin" in self.backend.run("ls /").stdout

    def tearDown(self):
        self.backend.tearDown()
