import unittest
from pathlib import Path

from WinJobster import Job, CallFailedException


class RunStopApp(unittest.TestCase):
    EXISTING_APP_PATH = "cmd.exe"
    NON_EXISTING_APP_PATH = ""

    @classmethod
    def setUpClass(cls):
        cls.job = Job()

    def tearDown(self):
        self.job.kill()

    def test_run_and_stop(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)

    def test_run_and_stop_with_path(self):
        cmdline = Path(self.EXISTING_APP_PATH)
        job = self.job
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)

    def test_run_and_stop_in_script_dir(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.start_process(cmdline, working_directory=None)
        self.assertTrue(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)

    def test_fail_run(self):
        cmdline = self.NON_EXISTING_APP_PATH
        job = self.job
        self.assertRaises(CallFailedException, job.start_process, cmdline)
        self.assertFalse(job.is_alive)

    def test_fail_kill(self):
        job = self.job
        self.assertFalse(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)

    def test_stop_before_run_and_rerun(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.kill()
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)

    def test_run_twice(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.start_process(cmdline)  # Memory leak
        self.assertTrue(job.is_alive)
        job.kill()
        self.assertFalse(job.is_alive)


if __name__ == '__main__':
    unittest.main()
