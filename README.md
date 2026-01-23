# PAN Card Validator

A Python package to validate and decode Indian PAN (Permanent Account Number) card numbers.

## Features

- ✅ Validate PAN card numbers according to Indian Income Tax standards
- 🔍 Decode PAN structure and extract meaningful information
- 📝 Detailed breakdown of each character's meaning
- 🖥️ Command-line interface for quick validation
- 🐍 Simple Python API for integration
- 🚀 Zero dependencies
- 💯 Comprehensive validation with detailed error messages

## Installation

```bash
pip install pancard
```

## Quick Start

### Command Line Usage

```bash
# Validate a PAN
pancard ABCDE1234F --validate

# Decode a PAN (default behavior)
pancard ABCDE1234F

# Get a summary
pancard ABCDE1234F --summary

# Output as JSON
pancard ABCDE1234F --json
```

### Python API Usage

```python
from pancard import validate_pan, decode_pan, PANValidator, PANDecoder

# Quick validation
is_valid = validate_pan("ABCDE1234F")
print(f"Valid: {is_valid}")

# Quick decode
info = decode_pan("ABCDE1234F")
print(info)

# Using validator class
validator = PANValidator()
is_valid = validator.validate("ABCDE1234F")

# Strict validation with exceptions
try:
    validator.validate_strict("ABCDE1234F")
    print("PAN is valid!")
except InvalidPANError as e:
    print(f"Invalid PAN: {e}")

# Using decoder class
decoder = PANDecoder()
decoded_info = decoder.decode("ABCDE1234F")
print(decoded_info)

# Get human-readable summary
summary = decoder.get_summary("ABCDE1234F")
print(summary)
```

## PAN Structure Explanation

A PAN is a 10-character alphanumeric identifier with the format: **AAAAA9999A**

### Character Breakdown:

1. **First 3 characters (AAA)**: Alphabetic series running from AAA to ZZZ
2. **4th character**: Type of PAN holder
   - P = Individual (Person)
   - C = Company
   - H = Hindu Undivided Family (HUF)
   - F = Firm/Partnership
   - A = Association of Persons (AOP)
   - T = Trust
   - B = Body of Individuals (BOI)
   - L = Local Authority
   - J = Artificial Juridical Person
   - G = Government

3. **5th character**: First letter of PAN holder's last name/surname
4. **Next 4 characters (6-9)**: Sequential numbers from 0001 to 9999
5. **Last character**: Alphabetic check digit

### Example

For PAN `ABCPE1234K`:
- `ABC` - Alphabetic series
- `P` - Individual person
- `E` - Surname starts with 'E'
- `1234` - Unique sequential number
- `K` - Check digit

## API Reference

### Functions

#### `validate_pan(pan_number: str) -> bool`
Validates a PAN card number.

#### `decode_pan(pan_number: str) -> dict`
Decodes a PAN card number and returns detailed information.

### Classes

#### `PANValidator`
- `validate(pan_number: str) -> bool`: Basic validation
- `validate_strict(pan_number: str) -> bool`: Strict validation with exceptions

#### `PANDecoder`
- `decode(pan_number: str) -> dict`: Decode PAN structure
- `get_summary(pan_number: str) -> str`: Get human-readable summary

### Exceptions

#### `InvalidPANError`
Raised when PAN validation fails in strict mode.

## Decoded Information Format

```python
{
    'pan_number': 'ABCPE1234K',
    'is_valid': True,
    'structure': {
        'pattern': 'AAAAA9999A',
        'total_length': 10,
        'alphabets_count': 6,
        'digits_count': 4
    },
    'holder_type': {
        'code': 'P',
        'type': 'Individual (Person)',
        'description': 'Individual taxpayer (most common type)'
    },
    'components': {
        'first_three_letters': {...},
        'fourth_letter': {...},
        'fifth_letter': {...},
        'next_four_digits': {...},
        'last_letter': {...}
    },
    'detailed_breakdown': [...]
}
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/yourusername/pancard.git
cd pancard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 pancard/
black pancard/ --check
mypy pancard/
```

### Running Tests

```bash
pytest tests/ -v
pytest --cov=pancard tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This package is for educational and validation purposes only. Always verify PAN details with official Income Tax Department resources for critical applications.

## Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/yourusername/pancard/issues).

## Acknowledgments

- Income Tax Department of India for PAN structure documentation
- Python community for inspiration and support