import unittest
import io
import sys
from redirect import Redirect

class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        stdout_capture = io.StringIO()
        with Redirect(stdout=stdout_capture):
            print('Hello stdout')
        self.assertEqual(stdout_capture.getvalue().strip(), 'Hello stdout')

    def test_redirect_stderr(self):
        stderr_capture = io.StringIO()
        with Redirect(stderr=stderr_capture):
            print('Hello stderr', file=sys.stderr)
        self.assertEqual(stderr_capture.getvalue().strip(), 'Hello stderr')

    def test_redirect_both(self):
        out = io.StringIO()
        err = io.StringIO()
        with Redirect(stdout=out, stderr=err):
            print('to out')
            print('to err', file=sys.stderr)
        self.assertEqual(out.getvalue().strip(), 'to out')
        self.assertEqual(err.getvalue().strip(), 'to err')

    def test_no_redirect(self):
        out = io.StringIO()
        err = io.StringIO()
        old_out = sys.stdout
        old_err = sys.stderr
        with Redirect():
            self.assertEqual(sys.stdout, old_out)
            self.assertEqual(sys.stderr, old_err)

if __name__ == '__main__':
    unittest.main()
