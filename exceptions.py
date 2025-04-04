# exceptions.py

class LookupError(Exception):
    """Base class for lookup-related exceptions."""
    pass

class VLookupError(LookupError):
    """Exception raised for errors in the VLOOKUP function."""
    def __init__(self, message="VLOOKUP operation failed."):
        self.message = message
        super().__init__(self.message)

class XLookupError(LookupError):
    """Exception raised for errors in the XLOOKUP function."""
    def __init__(self, message="XLOOKUP operation failed."):
        self.message = message
        super().__init__(self.message)