import pytest
from moduleframework import module_framework


def test_simple():
    backend, moduletype = module_framework.get_backend()
    backend.setUp()
    backend.start()
    assert "bin" in backend.run("ls /").stdout
    backend.tearDown()

