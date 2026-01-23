"""
PAN Card Decoder Module
Decodes the meaning of different characters in Indian PAN card numbers
"""

from .validator import PANValidator
from .exceptions import InvalidPANError

class PANDecoder:
    """
    Decoder class for Indian PAN card numbers
    Explains the meaning of each character in the PAN
    """
    
    def __init__(self):
        self.validator = PANValidator()
        
        # Mapping for the fourth character (holder type)
        self.holder_types = {
            'P': 'Individual (Person)',
            'C': 'Company',
            'H': 'Hindu Undivided Family (HUF)',
            'F': 'Firm/Partnership Firm',
            'A': 'Association of Persons (AOP)',
            'T': 'Trust (AOP)',
            'B': 'Body of Individuals (BOI)',
            'L': 'Local Authority',
            'J': 'Artificial Juridical Person',
            'G': 'Government'
        }
        
        # Mapping for the fifth character (name initial)
        self.name_info = {
            'description': 'First letter of PAN holder\'s last name/surname'
        }
    
    def decode(self, pan_number):
        """
        Decode a PAN card number and return its components
        
        Args:
            pan_number (str): PAN card number to decode
            
        Returns:
            dict: Dictionary containing decoded information
            
        Raises:
            InvalidPANError: If PAN is invalid
        """
        if not pan_number:
            raise InvalidPANError("PAN number cannot be empty")
        
        pan_number = str(pan_number).strip().upper()
        
        # Validate before decoding
        if not self.validator.validate(pan_number):
            raise InvalidPANError(f"Invalid PAN format: {pan_number}")
        
        decoded = {
            'pan_number': pan_number,
            'is_valid': True,
            'structure': self._get_structure_info(pan_number),
            'components': self._get_components(pan_number),
            'holder_type': self._get_holder_type(pan_number),
            'detailed_breakdown': self._get_detailed_breakdown(pan_number)
        }
        
        return decoded
    
    def _get_structure_info(self, pan_number):
        """
        Get structural information about the PAN
        
        Args:
            pan_number (str): Valid PAN number
            
        Returns:
            dict: Structure information
        """
        return {
            'pattern': 'AAAAA9999A',
            'total_length': 10,
            'alphabets_count': 6,
            'digits_count': 4,
            'format': f"{pan_number[:5]} (alphabets) + {pan_number[5:9]} (digits) + {pan_number[9]} (alphabet)"
        }
    
    def _get_components(self, pan_number):
        """
        Get individual components of the PAN
        
        Args:
            pan_number (str): Valid PAN number
            
        Returns:
            dict: Components of the PAN
        """
        return {
            'first_three_letters': {
                'value': pan_number[:3],
                'meaning': 'Alphabetic series running from AAA to ZZZ'
            },
            'fourth_letter': {
                'value': pan_number[3],
                'meaning': self.holder_types.get(pan_number[3], 'Unknown'),
                'category': 'Status of the PAN holder'
            },
            'fifth_letter': {
                'value': pan_number[4],
                'meaning': 'First character of the PAN holder\'s last name/surname',
                'category': 'Name initial'
            },
            'next_four_digits': {
                'value': pan_number[5:9],
                'meaning': 'Sequential number running from 0001 to 9999',
                'category': 'Unique identification number'
            },
            'last_letter': {
                'value': pan_number[9],
                'meaning': 'Alphabetic check digit',
                'category': 'Check character for verification'
            }
        }
    
    def _get_holder_type(self, pan_number):
        """
        Get detailed holder type information
        
        Args:
            pan_number (str): Valid PAN number
            
        Returns:
            dict: Holder type information
        """
        fourth_char = pan_number[3]
        return {
            'code': fourth_char,
            'type': self.holder_types.get(fourth_char, 'Unknown'),
            'description': self._get_holder_description(fourth_char)
        }
    
    def _get_holder_description(self, code):
        """
        Get detailed description for holder type
        
        Args:
            code (str): Fourth character of PAN
            
        Returns:
            str: Detailed description
        """
        descriptions = {
            'P': 'Individual taxpayer (most common type)',
            'C': 'Company registered under the Companies Act',
            'H': 'Hindu Undivided Family - a specific form of family arrangement recognized under Hindu Law',
            'F': 'Partnership Firm or Limited Liability Partnership',
            'A': 'Association of Persons or a body of individuals or a local authority or an artificial juridical person',
            'T': 'Trust entities including public or private trusts',
            'B': 'Body of Individuals - group of individuals carrying on business',
            'L': 'Local Authority like Municipalities, Panchayats, etc.',
            'J': 'Artificial Juridical Person not covered above',
            'G': 'Government agencies and departments'
        }
        return descriptions.get(code, 'Unknown holder type')
    
    def _get_detailed_breakdown(self, pan_number):
        """
        Get a detailed character-by-character breakdown
        
        Args:
            pan_number (str): Valid PAN number
            
        Returns:
            list: List of character information
        """
        breakdown = []
        
        for i, char in enumerate(pan_number):
            position = i + 1
            
            if i < 3:
                info = {
                    'position': position,
                    'character': char,
                    'type': 'Alphabet',
                    'purpose': 'Part of alphabetic series (AAA-ZZZ)'
                }
            elif i == 3:
                info = {
                    'position': position,
                    'character': char,
                    'type': 'Alphabet',
                    'purpose': f'Holder status - {self.holder_types.get(char, "Unknown")}'
                }
            elif i == 4:
                info = {
                    'position': position,
                    'character': char,
                    'type': 'Alphabet',
                    'purpose': 'First letter of surname/last name'
                }
            elif 5 <= i <= 8:
                info = {
                    'position': position,
                    'character': char,
                    'type': 'Digit',
                    'purpose': f'Sequential number (digit {i-4} of 4)'
                }
            else:  # i == 9
                info = {
                    'position': position,
                    'character': char,
                    'type': 'Alphabet',
                    'purpose': 'Check digit for validation'
                }
            
            breakdown.append(info)
        
        return breakdown
    
    def get_summary(self, pan_number):
        """
        Get a human-readable summary of the PAN
        
        Args:
            pan_number (str): PAN card number
            
        Returns:
            str: Summary description
        """
        decoded = self.decode(pan_number)
        
        holder_type = decoded['holder_type']['type']
        fifth_char = decoded['components']['fifth_letter']['value']
        
        summary = (
            f"PAN {pan_number} belongs to a {holder_type}. "
            f"The surname/last name starts with '{fifth_char}'. "
            f"The unique identification number is {decoded['components']['next_four_digits']['value']}."
        )
        
        return summary