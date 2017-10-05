from moduleframework import module_framework
from moduleframework.helpers.container_helper import ContainerHelper
from moduleframework import common
from avocado.utils import process
from avocado import Test
import time

WAIT_TIME=15

class OneMachine(module_framework.ContainerAvocadoTest):
    """
    An example of collections testing.

    :avocado: enable
    """

    def testMariaDBDirExist(self):
        """
        Run a command on a host and test if a directory exists inside a container.
        """
        self.start()
        self.run("ls /var/lib/mysql")

    def testDefaultConfig(self):
        """
        Test the default container defined in config.yaml starts.
        """
        self.start()
        time.sleep(WAIT_TIME)
        command = "echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}"
        self.assertIn("1", self.runHost(command, shell=True).stdout)

    def testNonDefaultStartAction(self):
        """
        Test connection to a port different from the one in config.yaml.
        """
        docker_start = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.getConfig()["module"]["docker"]["start"] = docker_start
        self.start()
        time.sleep(WAIT_TIME)
        command = "echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}"
        self.assertIn("1", self.runHost(command, shell=True).stdout)

    def testThisFail(self):
        """
        Test if mysql is unable to connect to another port than defined.
        """
        docker_start = "docker run -p 3308:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.getConfig()["module"]["docker"]["start"] = docker_start
        self.start()
        time.sleep(WAIT_TIME)
        command = "echo select 1 | mysql -P 3307 -h 127.0.0.1 -u root -p{PASSWORD}"
        self.assertIn("t connect to MySQL server", \
                self.runHost(command, shell=True, ignore_status=True).stderr)


class OneMachineInSetup(module_framework.ContainerAvocadoTest):
    """
    An example of collections tesing with a modified setUp() method.
    Only one modificaion in a class is possible.

    :avocado: enable
    """

    def setUp(self):
        super(self.__class__,self).setUp()
        docker_start = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.getConfig()["module"]["docker"]["start"] = docker_start
        self.start()
        time.sleep(WAIT_TIME)

    def testDefaultConfig(self):
        """
        Test modified setUp()
        """
        command = "echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307"
        self.assertIn("1", self.runHost(command, shell=True).stdout)


class MultipleMachines(Test):
    """
    Test two containers running at the same time.

    :avocado: enable
    """

    def setUp(self):
        self.docker1 = ContainerHelper()
        self.docker1.setUp()
        self.docker2 = ContainerHelper()
        self.docker2.setUp()

    def testMultipleInstance(self):
        """
        Start and connect to two containers running on different ports.
        """
        self.docker1.start()
        docker_start = "docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD={PASSWORD}"
        self.docker2.config["module"]["docker"]["start"] = docker_start
        self.docker2.start()
        time.sleep(WAIT_TIME)
        command_one = "echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD}"
        command_two = "echo select 1 | mysql -h 127.0.0.1 -u root -p{PASSWORD} -P 3307"
        self.assertIn("1", process.run(command_one.format(**common.trans_dict), \
            shell=True).stdout)
        self.assertIn("1", process.run(command_two.format(**common.trans_dict), \
            shell=True).stdout)

    def tearDown(self):
        self.docker1.tearDown()
        self.docker2.tearDown()
