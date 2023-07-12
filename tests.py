import unittest

from Process import Process
from WinJobsterCallFailedException import WinJobsterCallFailedException


class RunStopApp(unittest.TestCase):
    EXISTING_APP_PATH = "cmd.exe"
    NON_EXISTING_APP_PATH = ""

    @classmethod
    def setUpClass(cls):
        cls.process = Process()

    def tearDown(self):
        self.process.kill()

    def test_run_and_stop(self):
        cmdline = self.EXISTING_APP_PATH
        process = self.process
        process.start(cmdline)
        self.assertTrue(process.is_alive)
        process.kill()
        self.assertFalse(process.is_alive)

    def test_fail_run(self):
        cmdline = self.NON_EXISTING_APP_PATH
        process = self.process
        self.assertRaises(WinJobsterCallFailedException, process.start, cmdline)
        self.assertFalse(process.is_alive)

    def test_fail_kill(self):
        process = self.process
        self.assertFalse(process.is_alive)
        process.kill()
        self.assertFalse(process.is_alive)

    def test_stop_before_run_and_rerun(self):
        cmdline = self.EXISTING_APP_PATH
        process = self.process
        process.kill()
        self.assertFalse(process.is_alive)
        process.start(cmdline)
        self.assertTrue(process.is_alive)
        process.kill()
        self.assertFalse(process.is_alive)
        process.start(cmdline)
        self.assertTrue(process.is_alive)

    def test_run_twice(self):
        cmdline = self.EXISTING_APP_PATH
        process = self.process
        self.assertFalse(process.is_alive)
        process.start(cmdline)
        self.assertTrue(process.is_alive)
        process.start(cmdline)  # Memory leak
        self.assertTrue(process.is_alive)
        process.kill()
        self.assertFalse(process.is_alive)


if __name__ == '__main__':
    unittest.main()
