"""
Command Line Interface for PAN Card validator
"""

import sys
import argparse
import json
from .validator import PANValidator
from .decoder import PANDecoder
from .exceptions import InvalidPANError

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Validate and decode Indian PAN card numbers',
        prog='pancard'
    )
    
    parser.add_argument(
        'pan',
        type=str,
        help='PAN card number to validate/decode'
    )
    
    parser.add_argument(
        '-v', '--validate',
        action='store_true',
        help='Only validate the PAN (default: validate and decode)'
    )
    
    parser.add_argument(
        '-d', '--decode',
        action='store_true',
        help='Decode the PAN and show detailed information'
    )
    
    parser.add_argument(
        '-s', '--summary',
        action='store_true',
        help='Show a summary of the PAN'
    )
    
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    args = parser.parse_args()
    
    validator = PANValidator()
    decoder = PANDecoder()
    
    try:
        # Default behavior: validate and decode
        if not args.validate and not args.decode and not args.summary:
            args.decode = True
        
        pan_number = args.pan.strip().upper()
        
        if args.validate:
            is_valid = validator.validate(pan_number)
            if args.json:
                print(json.dumps({'pan': pan_number, 'valid': is_valid}))
            else:
                if is_valid:
                    print(f"✓ {pan_number} is a valid PAN")
                else:
                    print(f"✗ {pan_number} is not a valid PAN")
            
            if not is_valid:
                sys.exit(1)
        
        if args.decode:
            try:
                decoded = decoder.decode(pan_number)
                if args.json:
                    print(json.dumps(decoded, indent=2))
                else:
                    print(f"\nPAN Card Analysis: {pan_number}")
                    print("=" * 50)
                    print(f"Valid: {decoded['is_valid']}")
                    print(f"Holder Type: {decoded['holder_type']['type']}")
                    print(f"Description: {decoded['holder_type']['description']}")
                    print("\nCharacter Breakdown:")
                    print("-" * 30)
                    for item in decoded['detailed_breakdown']:
                        print(f"Position {item['position']}: '{item['character']}' - {item['purpose']}")
            except InvalidPANError as e:
                if args.json:
                    print(json.dumps({'error': str(e)}, indent=2))
                else:
                    print(f"Error: {e}")
                sys.exit(1)
        
        if args.summary:
            try:
                summary = decoder.get_summary(pan_number)
                if args.json:
                    print(json.dumps({'pan': pan_number, 'summary': summary}))
                else:
                    print(f"\nSummary: {summary}")
            except InvalidPANError as e:
                if args.json:
                    print(json.dumps({'error': str(e)}, indent=2))
                else:
                    print(f"Error: {e}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()