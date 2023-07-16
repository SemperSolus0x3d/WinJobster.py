import unittest
from pathlib import Path

from WinJobster import Job, CallFailedException


class RunStopApp(unittest.TestCase):
    EXISTING_APP_PATH = "notepad.exe"
    NON_EXISTING_APP_PATH = ""

    def setUp(self):
        self.job = Job()

    def tearDown(self):
        del self.job

    def test_run_and_stop(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)

    def test_count_processes(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        self.assertEquals(0, len(job.process_ids))
        job.start_process(cmdline)
        self.assertEquals(1, len(job.process_ids))
        job.start_process(cmdline)
        self.assertEquals(2, len(job.process_ids))
        job.terminate()
        self.assertEquals(0, len(job.process_ids))

    def test_existing_processes_used(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.start_process(cmdline)
        job.start_process(cmdline)
        job.start_process(cmdline)
        self.assertEquals(3, len(job.process_ids))
        for pid in job.process_ids:
            self.assertNotEquals(0, len(job.process_ids))

    def test_run_and_stop_with_path(self):
        cmdline = Path(self.EXISTING_APP_PATH)
        job = self.job
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)

    def test_run_and_stop_in_script_dir(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.start_process(cmdline, working_directory=None)
        self.assertTrue(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)

    def test_fail_run(self):
        cmdline = self.NON_EXISTING_APP_PATH
        job = self.job
        self.assertRaises(CallFailedException, job.start_process, cmdline)
        self.assertFalse(job.is_alive)

    def test_fail_kill(self):
        job = self.job
        self.assertFalse(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)

    # @unittest.skip('Will fix later')  # Dirty-patched, TODO: Fix properly
    def test_stop_before_run_and_rerun(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        job.terminate()
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)

    def test_run_twice(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.start_process(cmdline)
        self.assertTrue(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)

    def test_terminate_twice(self):
        cmdline = self.EXISTING_APP_PATH
        job = self.job
        self.assertFalse(job.is_alive)
        job.start_process(cmdline)
        job.terminate()
        self.assertFalse(job.is_alive)
        job.terminate()
        self.assertFalse(job.is_alive)


if __name__ == '__main__':
    unittest.main()
