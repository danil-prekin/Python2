import sys

class Redirect:
    def __init__(self, stdout=None, stderr=None):
        self.new_stdout = stdout
        self.new_stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        if self.new_stdout is not None:
            self.old_stdout = sys.stdout
            sys.stdout = self.new_stdout
        if self.new_stderr is not None:
            self.old_stderr = sys.stderr
            sys.stderr = self.new_stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.new_stdout is not None:
            sys.stdout = self.old_stdout
        if self.new_stderr is not None:
            sys.stderr = self.old_stderr
