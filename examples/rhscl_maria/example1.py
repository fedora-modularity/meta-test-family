
from moduleframework import module_framework
from moduleframework.helpers.container_helper import ContainerHelper
from moduleframework import common
from avocado.utils import process
from avocado import Test
import time

WAIT_TIME=10

class OneMachine(module_framework.AvocadoTest):
    """
    Basic, the most straightforward example how to use it with collections,
    many configs, and similar tests

    :avocado: enable
    """

    def testMariaDBDirExist(self):
        """
        run command on host and test if directory inside container exist

        :return:
        """
        self.start()
        self.run("ls /var/lib/mysql")

    def testDefaultConfig(self):
        """
        Test default container started based on config.yaml params

        :return:
        """
        self.start()
        time.sleep(WAIT_TIME)
        self.assertIn("1", self.runHost("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}", shell=True).stdout)

    def testNonDefaultStartAction(self):
        """
        Nontrivial case similart to testDefaultConfig.
        Redefined start action to custom one (port forwarded to 3307)

        :return:
        """
        self.getConfig()["module"]["docker"]["start"]="docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.start()
        time.sleep(WAIT_TIME)
        self.assertIn("1", self.runHost("echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}", shell=True).stdout)

    def testThisFail(self):
        """
        Test if mysql is unable to connect to another port than defined

        :return:
        """
        self.getConfig()["module"]["docker"]["start"]="docker run -p 3308:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.start()
        time.sleep(WAIT_TIME)
        self.assertIn("t connect to MySQL server", self.runHost("echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}",
                                        shell=True, ignore_status=True).stderr)


class OneMachineInSetup(module_framework.AvocadoTest):
    """
    Example of test for collections with custom action in own setUp() method.
    It is cleaner, but it allow to have just one modificaion in one class

    :avocado: enable
    """

    def setUp(self):
        super(self.__class__,self).setUp()
        self.getConfig()["module"]["docker"]["start"] = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.start()
        time.sleep(WAIT_TIME)

    def testDefaultConfig(self):
        """
        simple test
        :return:
        """
        self.assertIn("1", self.runHost("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307", shell=True).stdout)


class MultipleMachines(Test):
    """
    Test more container running in same time.
    Low level, the most complex example.
    Allow to define more than just one per class conotainers and test if both are running

    :avocado: enable
    """

    def setUp(self):
        self.docker1 = ContainerHelper()
        self.docker1.setUp()
        self.docker2 = ContainerHelper()
        self.docker2.setUp()

    def testMultipleInstance(self):
        """
        start containers and connect to both of them, they are running on various ports

        :return:
        """
        self.docker1.start()
        self.docker2.config["module"]["docker"]["start"] = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.docker2.start()
        time.sleep(10)
        self.assertIn("1", process.run("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}".format(**common.trans_dict), shell=True).stdout)
        self.assertIn("1", process.run("echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307".format(**common.trans_dict), shell=True).stdout)

    def tearDown(self):
        self.docker1.tearDown()
        self.docker2.tearDown()




