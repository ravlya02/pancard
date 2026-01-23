"""
Custom exceptions for PAN Card validation
"""

class PANCardError(Exception):
    """Base exception for PAN card related errors"""
    pass

class InvalidPANError(PANCardError):
    """Exception raised when PAN card number is invalid"""
    
    def __init__(self, message="Invalid PAN card number"):
        self.message = message
        super().__init__(self.message)

class PANDecodingError(PANCardError):
    """Exception raised when PAN card cannot be decoded"""
    
    def __init__(self, message="Unable to decode PAN card"):
        self.message = message
        super().__init__(self.message)