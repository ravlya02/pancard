"""
PAN Card Validator Module
Validates Indian PAN card numbers according to the standard format
"""

import re
from .exceptions import InvalidPANError

class PANValidator:
    """
    Validator class for Indian PAN card numbers
    
    PAN Structure: AAAAA9999A
    - First 5 characters: Alphabets
    - Next 4 characters: Numerals
    - Last character: Alphabet
    """
    
    # PAN card regex pattern
    PAN_PATTERN = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    
    def __init__(self):
        self.pattern = re.compile(self.PAN_PATTERN)
    
    def validate(self, pan_number):
        """
        Validate a PAN card number
        
        Args:
            pan_number (str): PAN card number to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            InvalidPANError: If PAN format is invalid with details
        """
        if not pan_number:
            return False
        
        # Convert to uppercase for validation
        pan_number = str(pan_number).strip().upper()
        
        # Check length
        if len(pan_number) != 10:
            return False
        
        # Check pattern
        if not self.pattern.match(pan_number):
            return False
        
        # Additional validation rules
        return self._validate_structure(pan_number)
    
    def _validate_structure(self, pan_number):
        """
        Validate the structure and business rules of PAN
        
        Args:
            pan_number (str): PAN card number
            
        Returns:
            bool: True if structure is valid
        """
        # Fourth character should be one of these based on holder type
        valid_fourth_chars = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']
        
        if pan_number[3] not in valid_fourth_chars:
            return False
        
        return True
    
    def validate_strict(self, pan_number):
        """
        Strict validation that raises exceptions with details
        
        Args:
            pan_number (str): PAN card number to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            InvalidPANError: With specific error details
        """
        if not pan_number:
            raise InvalidPANError("PAN number cannot be empty")
        
        pan_number = str(pan_number).strip().upper()
        
        if len(pan_number) != 10:
            raise InvalidPANError(f"PAN must be exactly 10 characters, got {len(pan_number)}")
        
        if not pan_number[:5].isalpha():
            raise InvalidPANError("First 5 characters must be alphabets")
        
        if not pan_number[5:9].isdigit():
            raise InvalidPANError("Characters 6-9 must be digits")
        
        if not pan_number[9].isalpha():
            raise InvalidPANError("Last character must be an alphabet")
        
        valid_fourth_chars = {
            'P': 'Individual',
            'C': 'Company',
            'H': 'Hindu Undivided Family (HUF)',
            'F': 'Firm',
            'A': 'Association of Persons (AOP)',
            'T': 'Trust',
            'B': 'Body of Individuals (BOI)',
            'L': 'Local Authority',
            'J': 'Artificial Juridical Person',
            'G': 'Government'
        }
        
        if pan_number[3] not in valid_fourth_chars:
            raise InvalidPANError(
                f"Fourth character '{pan_number[3]}' is invalid. "
                f"Must be one of: {', '.join(valid_fourth_chars.keys())}"
            )
        
        return True