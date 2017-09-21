import unittest
from moduleframework import module_framework

class TestSimple(unittest.TestCase):

    def setUp(self):
        self.backend, self.moduletype = module_framework.get_backend()
        self.backend.setUp()
        self.backend.start()

    def tearDown(self):
        self.backend.tearDown()

    def test_simple(self):
        self.assertIn("bin", self.backend.run("ls /").stdout)

if __name__ == '__main__':
    unittest.main()