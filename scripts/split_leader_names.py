#!/usr/bin/env python3
"""
Script to split leader names from example_leaders.txt into separate first names and surnames files.
"""

import os
import re

def split_leader_names(input_file, output_dir):
    """Split leader names into first names and surnames."""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]
    
    first_names = set()
    surnames = set()
    
    for name in names:
        # Clean up the name and split by spaces
        clean_name = name.strip()
        parts = clean_name.split()
        
        if len(parts) >= 2:
            # First part is first name
            first_name = parts[0]
            first_names.add(first_name)
            
            # Last part is surname (handle compound surnames)
            surname = parts[-1]
            surnames.add(surname)
            
            # If there are middle parts, check for common patterns
            if len(parts) > 2:
                for part in parts[1:-1]:
                    # Skip common particles and titles
                    if part.lower() not in ['of', 'the', 'van', 'de', 'der', 'ten', 'op', 'aan', 'in', "'t", 'la']:
                        # Could be either first name or part of surname
                        # Add to first names if it looks like a first name
                        if not part.startswith("'") and not part.endswith("'"):
                            first_names.add(part)
        
        elif len(parts) == 1:
            # Single name - treat as first name
            first_names.add(parts[0])
    
    # Write first names file
    first_names_file = os.path.join(output_dir, 'example_leaders_firstnames.txt')
    with open(first_names_file, 'w', encoding='utf-8') as f:
        for name in sorted(first_names):
            f.write(f"{name}\n")
    
    # Write surnames file
    surnames_file = os.path.join(output_dir, 'example_leaders_surnames.txt')
    with open(surnames_file, 'w', encoding='utf-8') as f:
        for name in sorted(surnames):
            f.write(f"{name}\n")
    
    print(f"Processed {len(names)} names")
    print(f"Extracted {len(first_names)} unique first names")
    print(f"Extracted {len(surnames)} unique surnames")
    print(f"First names saved to: {first_names_file}")
    print(f"Surnames saved to: {surnames_file}")

def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'example_leaders.txt')
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return
    
    split_leader_names(input_file, script_dir)

if __name__ == "__main__":
    main()
