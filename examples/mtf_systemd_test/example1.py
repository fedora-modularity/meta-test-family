from avocado import Test
from mtf.backend.nspawn import Image, Container
from avocado.utils import process
import os

# Centos Hack. it does not support wait athought fedora support it ()
# [stderr] Failed to start transient service unit: Cannot set property AddRef, or unknown property.
# force disable wait support
Container._run_systemdrun_decide = lambda x:False

if os.environ.get("REPOS"):
    repo = os.environ.get("REPOS").split(";")
else:
    repo = ["http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/26/Everything/x86_64/os/"]
packages = ["bash", "iproute", "passwd"]

class testSystemd1(Test):
    c1 = None
    cname = "contA"
    sname = "nonexistingservice"
    exitcode = 2
    def setUp(self):
        loc1 = "/tmp/dddd1"
        self.i1 = Image(repos=repo, packageset=packages, location=loc1, ignore_installed=True)
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine()

    def test_basic(self):
        self.assertIn("sbin",self.c1.execute(command="ls /").stdout)

    def test_status(self):
        self.assertIn("systemd-logind", self.c1.execute(command="systemctl status").stdout)
        self.assertNotIn("gnome",self.c1.execute(command="systemctl status").stdout)

    def test_exception(self):
        self.assertRaises(process.CmdError, self.c1.execute, "badcommand")
        self.assertRaises(process.CmdError, self.c1.execute, "exit %s" % self.exitcode)
        self.assertEqual(self.exitcode,self.c1.execute(command = "exit %s" % self.exitcode, ignore_status=True).exit_status)

    def test_nonexisting_service_start(self):
        self.assertEqual(5, self.c1.execute(command="systemctl start %s" % self.sname, ignore_status=True).exit_status)

    def test_nonexisting_service_status(self):
        self.assertEqual(4, self.c1.execute(command="systemctl status %s" % self.sname, ignore_status=True).exit_status)

    def test_nonexisting_service_stop(self):
        self.assertEqual(5, self.c1.execute(command="systemctl stop %s" % self.sname, ignore_status=True).exit_status)

    def test_nonexisting_action(self):
        self.assertEqual(1, self.c1.execute(command="systemctl %s" % self.sname, ignore_status=True).exit_status)

    def tearDown(self):
        self.c1.stop()

class testSystemd2(Test):
    """
    It tests Container object and his abilities to run various commands
    """
    c1 = None
    cname = "contA"
    def setUp(self):
        loc1 = "/tmp/dddd1"
        self.i1 = Image(repos=repo, packageset=packages, location=loc1, ignore_installed=True)

    def test_basic(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.assertIn("sbin", self.c1.boot_machine(boot_cmd="ls /", wait_finish=True).get_stdout())
        self.c1.boot_machine(boot_cmd="""bash -c "echo redhat | passwd --stdin" """, wait_finish=True)
        self.c1.boot_machine()
        self.assertIn("sbin",self.c1.execute(command="ls /").stdout)

    def tearDown(self):
        self.c1.stop()


class testSystemdMultihost(Test):
    c1 = None
    c2 = None
    loc1 = "/tmp/dddd1"
    loc2 = "/tmp/dddd2"
    loc3 = "/tmp/dddd3"

    def setUp(self):
        self.i1 = Image(repos=repo, packageset=packages, location=self.loc1, ignore_installed=True)
        self.c1 = Container(image=self.i1.create_snapshot(destination=self.loc2), name=self.loc2.split('/')[-1])
        self.c1.boot_machine()
        self.c2 = Container(image=self.i1.create_snapshot(destination=self.loc3), name=self.loc3.split('/')[-1])
        self.c2.boot_machine()

    def test_basic(self):
        process.run("machinectl status %s" % self.loc2.split('/')[-1])
        process.run("machinectl status %s" % self.loc3.split('/')[-1])
        self.c1.stop()
        self.c2.stop()
        self.assertRaises(process.CmdError, process.run, "machinectl status %s" % self.loc2.split('/')[-1])
        self.assertRaises(process.CmdError, process.run, "machinectl status %s" % self.loc3.split('/')[-1])

    def tearDown(self):
        self.c1.rm()
        self.c2.rm()
