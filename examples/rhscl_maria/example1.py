
from moduleframework import module_framework
from moduleframework.helpers.container_helper import ContainerHelper
from moduleframework import common
from avocado.utils import process
from avocado import Test
import time


class OneMachine(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def testMariaDBDirExist(self):
        self.start()
        self.run("ls /var/lib/mysql")

    def testDefaultConfig(self):
        self.start()
        time.sleep(10)
        self.assertIn("1", self.runHost("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}", shell=True).stdout)

    def testNonDefaultStartAction(self):
        self.getConfig()["module"]["docker"]["start"]="docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.start()
        time.sleep(10)
        self.assertIn("1", self.runHost("echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}", shell=True).stdout)

    def testThisFail(self):
        self.getConfig()["module"]["docker"]["start"]="docker run -p 3308:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.start()
        time.sleep(10)
        self.assertIn("t connect to MySQL server", self.runHost("echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}",
                                        shell=True, ignore_status=True).stderr)


class OneMachineInSetup(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def setUp(self):
        super(self.__class__,self).setUp()
        self.getConfig()["module"]["docker"]["start"] = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"

    def testDefaultConfig(self):
        self.start()
        self.assertIn("1", self.runHost("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307", shell=True).stdout)


class MultipleMachines(Test):
    """
    :avocado: enable
    """

    def setUp(self):
        self.docker1 = ContainerHelper()
        self.docker1.setUp()
        self.docker2 = ContainerHelper()
        self.docker2.setUp()

    def testMultipleInstance(self):
        self.docker1.start()
        self.docker2.config["module"]["docker"]["start"] = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.docker2.start()
        time.sleep(10)
        self.assertIn("1", process.run("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}".format(**common.trans_dict), shell=True).stdout)
        self.assertIn("1", process.run("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307".format(**common.trans_dict), shell=True).stdout)

    def tearDown(self):
        self.docker1.tearDown()
        self.docker2.tearDown()




