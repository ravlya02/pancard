"""
Test suite for pancard package
"""

import pytest
from pancard import PANValidator, PANDecoder, validate_pan, decode_pan
from pancard.exceptions import InvalidPANError

class TestPANValidator:
    """Test cases for PANValidator class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.validator = PANValidator()
        self.valid_pans = [
            "ABCPE1234K",
            "ZZZZZ9999Z",
            "AAAAA0001A",
            "XYZPC5678L",
            "DEFCH7890M",
        ]
        self.invalid_pans = [
            "ABCDE12345",  # 11 characters
            "ABCD1234K",   # 9 characters
            "12CPE1234K",  # Starts with numbers
            "ABCPE12K4K",  # Number in wrong position
            "ABCPX1234K",  # Invalid 4th character
            "abcpe1234k",  # Lowercase (should be converted)
            "",            # Empty
            None,          # None
            "ABC PE1234K", # Contains space
        ]
    
    def test_valid_pans(self):
        """Test validation of valid PAN numbers"""
        for pan in self.valid_pans:
            assert self.validator.validate(pan) == True, f"Failed for {pan}"
    
    def test_invalid_pans(self):
        """Test validation of invalid PAN numbers"""
        for pan in self.invalid_pans:
            if pan and not " " in str(pan):
                assert self.validator.validate(pan) == False, f"Failed for {pan}"
    
    def test_case_insensitive(self):
        """Test that validation is case-insensitive"""
        assert self.validator.validate("abcpe1234k") == True
        assert self.validator.validate("ABCPE1234K") == True
    
    def test_validate_strict(self):
        """Test strict validation with exceptions"""
        # Valid PAN should not raise exception
        assert self.validator.validate_strict("ABCPE1234K") == True
        
        # Invalid PANs should raise exceptions
        with pytest.raises(InvalidPANError, match="cannot be empty"):
            self.validator.validate_strict("")
        
        with pytest.raises(InvalidPANError, match="exactly 10 characters"):
            self.validator.validate_strict("ABC123")
        
        with pytest.raises(InvalidPANError, match="First 5 characters must be alphabets"):
            self.validator.validate_strict("ABC1E1234K")
        
        with pytest.raises(InvalidPANError, match="Characters 6-9 must be digits"):
            self.validator.validate_strict("ABCPEABCDK")
        
        with pytest.raises(InvalidPANError, match="Last character must be an alphabet"):
            self.validator.validate_strict("ABCPE12345")
        
        with pytest.raises(InvalidPANError, match="Fourth character"):
            self.validator.validate_strict("ABCXE1234K")
    
    def test_fourth_character_validation(self):
        """Test validation of fourth character (holder type)"""
        valid_fourth_chars = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']
        
        for char in valid_fourth_chars:
            pan = f"ABC{char}E1234K"
            assert self.validator.validate(pan) == True, f"Failed for fourth char: {char}"
        
        # Test invalid fourth character
        assert self.validator.validate("ABCXE1234K") == False


class TestPANDecoder:
    """Test cases for PANDecoder class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.decoder = PANDecoder()
    
    def test_decode_valid_pan(self):
        """Test decoding of valid PAN"""
        result = self.decoder.decode("ABCPE1234K")
        
        assert result['pan_number'] == "ABCPE1234K"
        assert result['is_valid'] == True
        assert result['holder_type']['code'] == 'P'
        assert result['holder_type']['type'] == 'Individual (Person)'
        assert 'components' in result
        assert 'detailed_breakdown' in result
        assert 'structure' in result
    
    def test_decode_invalid_pan(self):
        """Test decoding of invalid PAN raises exception"""
        with pytest.raises(InvalidPANError):
            self.decoder.decode("INVALID123")
    
    def test_decode_components(self):
        """Test component extraction"""
        result = self.decoder.decode("XYZCH5678M")
        components = result['components']
        
        assert components['first_three_letters']['value'] == 'XYZ'
        assert components['fourth_letter']['value'] == 'C'
        assert components['fifth_letter']['value'] == 'H'
        assert components['next_four_digits']['value'] == '5678'
        assert components['last_letter']['value'] == 'M'
    
    def test_holder_types(self):
        """Test different holder types"""
        test_cases = {
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
        
        for code, expected_type in test_cases.items():
            pan = f"ABC{code}E1234K"
            result = self.decoder.decode(pan)
            assert result['holder_type']['code'] == code
            assert result['holder_type']['type'] == expected_type
    
    def test_get_summary(self):
        """Test summary generation"""
        summary = self.decoder.get_summary("ABCPE1234K")
        
        assert "Individual (Person)" in summary
        assert "1234" in summary
        assert "E" in summary
        assert "ABCPE1234K" in summary
    
    def test_detailed_breakdown(self):
        """Test detailed breakdown"""
        result = self.decoder.decode("ABCPE1234K")
        breakdown = result['detailed_breakdown']
        
        assert len(breakdown) == 10
        assert breakdown[0]['position'] == 1
        assert breakdown[0]['character'] == 'A'
        assert breakdown[3]['character'] == 'P'
        assert 'Individual' in breakdown[3]['purpose']
        assert breakdown[4]['character'] == 'E'
        assert 'surname' in breakdown[4]['purpose'].lower()


class TestModuleFunctions:
    """Test module-level convenience functions"""
    
    def test_validate_pan_function(self):
        """Test the validate_pan convenience function"""
        assert validate_pan("ABCPE1234K") == True
        assert validate_pan("INVALID") == False
        assert validate_pan("") == False
    
    def test_decode_pan_function(self):
        """Test the decode_pan convenience function"""
        result = decode_pan("ABCPE1234K")
        assert result['is_valid'] == True
        assert result['pan_number'] == "ABCPE1234K"
        
        with pytest.raises(InvalidPANError):
            decode_pan("INVALID")


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def setup_method(self):
        self.validator = PANValidator()
        self.decoder = PANDecoder()
    
    def test_whitespace_handling(self):
        """Test handling of whitespace"""
        assert self.validator.validate("  ABCPE1234K  ") == True
        assert self.validator.validate("ABCPE1234K\n") == True
        assert self.validator.validate("\tABCPE1234K") == True
    
    def test_special_characters(self):
        """Test that special characters invalidate PAN"""
        invalid_pans = [
            "ABCPE-1234K",
            "ABCPE@1234K",
            "ABCPE.1234K",
            "ABCPE 1234K",
            "ABCPE_1234K"
        ]
        
        for pan in invalid_pans:
            assert self.validator.validate(pan) == False
    
    def test_numeric_boundaries(self):
        """Test numeric portion boundaries"""
        assert self.validator.validate("ABCPE0000K") == True
        assert self.validator.validate("ABCPE9999K") == True
        assert self.validator.validate("ABCPE0001K") == True
    
    def test_alphabetic_boundaries(self):
        """Test alphabetic boundaries"""
        assert self.validator.validate("AAAAA0000A") == True
        assert self.validator.validate("ZZZZZ9999Z") == True
    
    def test_empty_and_none(self):
        """Test empty string and None handling"""
        assert self.validator.validate("") == False
        assert self.validator.validate(None) == False
        
        with pytest.raises(InvalidPANError):
            self.decoder.decode("")
        
        with pytest.raises(InvalidPANError):
            self.decoder.decode(None)