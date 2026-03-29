class BlockErrors:
    def __init__(self, errors):
        self.errors = errors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        if issubclass(exc_type, tuple(self.errors) if isinstance(self.errors, tuple) else self.errors):
            return True
        return False
