"""
PAN Card Validator Package
A Python package to validate and decode Indian PAN card numbers
"""

__version__ = "0.1.0"
__author__ = "Rahul Ratnaparkhi"
__email__ = "ravlya02@gmail.com"

from .validator import PANValidator
from .decoder import PANDecoder
from .exceptions import InvalidPANError

__all__ = ['PANValidator', 'PANDecoder', 'InvalidPANError', 'validate_pan', 'decode_pan']

def validate_pan(pan_number):
    """
    Quick validation function for PAN card number
    
    Args:
        pan_number (str): PAN card number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    validator = PANValidator()
    return validator.validate(pan_number)

def decode_pan(pan_number):
    """
    Quick decode function for PAN card number
    
    Args:
        pan_number (str): PAN card number to decode
        
    Returns:
        dict: Decoded information about the PAN
    """
    decoder = PANDecoder()
    return decoder.decode(pan_number)