#!/usr/bin/python

import os
import sys
import socket
import time
from avocado import utils
from avocado import main
machine_test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","base")
if not machine_test_dir in sys.path:
    sys.path.insert(1, machine_test_dir)
import moduleframework

class SanityCheck1(moduleframework.AvocadoTest):
    """
    :avocado: enable
    """
    def test1(self):
        self.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', self.config['service']['port']))
        s.sendall('set Test 0 100 4\r\n\n')
        #data = s.recv(1024)
        #print data
        
        s.sendall('get Test\r\n')
        #data = s.recv(1024)
        #print data
        s.close()
        
    def test2(self):
        self.start()
        self.run("ls /")

if __name__ == '__main__':
    main()
    
    
