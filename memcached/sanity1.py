#!/usr/bin/python

import socket
from avocado import main
from avocado.core import exceptions
import moduleframework


class SanityCheck1(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """

    def test1(self):
        self.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', self.getConfig()['service']['port']))
        s.sendall('set Test 0 100 4\r\n\n')
        #data = s.recv(1024)
        # print data

        s.sendall('get Test\r\n')
        #data = s.recv(1024)
        # print data
        s.close()

    def test2(self):
        self.start()
        self.run("ls / | grep bin")

    def test3GccSkipped(self):
        moduleframework.skipTestIf("gcc" not in self.getActualProfile())
        self.start()
        self.run("gcc -v")

if __name__ == '__main__':
    main()
