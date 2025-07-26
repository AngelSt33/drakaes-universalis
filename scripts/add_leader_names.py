#!/usr/bin/env python3
"""
Script to add 10 additional random leader names to all EU4 country files.
Combines random first names and surnames from the split leader files.
"""

import os
import random
import re

def load_names_from_file(file_path):
    """Load names from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f if line.strip()]
        return names
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []

def generate_random_leader_name(first_names, surnames):
    """Generate a random leader name by combining first name and surname."""
    first_name = random.choice(first_names)
    surname = random.choice(surnames)
    return f"{first_name} {surname}"

def get_existing_leader_names(content):
    """Extract existing leader names from country file content."""
    # Find the leader_names section
    leader_match = re.search(r'leader_names\s*=\s*\{([^}]*)\}', content, re.DOTALL)
    if leader_match:
        leader_content = leader_match.group(1)
        # Extract quoted names
        names = re.findall(r'"([^"]+)"', leader_content)
        return names
    return []

def format_leader_names(names):
    """Format leader names for the leader_names section."""
    formatted_names = '\n'.join([f'\t"{name}"' for name in names])
    return f"{{\n{formatted_names}\n}}"

def process_country_file(file_path, first_names, surnames):
    """Process a single country file to add additional leader names."""
    print(f"Processing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get existing leader names
    existing_names = get_existing_leader_names(content)
    print(f"  - Current leader names: {len(existing_names)}")
    
    # Generate 10 additional names
    additional_names = []
    attempts = 0
    max_attempts = 1000  # Prevent infinite loop
    
    while len(additional_names) < 10 and attempts < max_attempts:
        new_name = generate_random_leader_name(first_names, surnames)
        # Ensure we don't duplicate existing names
        if new_name not in existing_names and new_name not in additional_names:
            additional_names.append(new_name)
        attempts += 1
    
    # Combine existing and new names
    all_names = existing_names + additional_names
    formatted_leaders = format_leader_names(all_names)
    
    # Replace the leader_names section
    content = re.sub(r'leader_names\s*=\s*\{[^}]*\}', f'leader_names = {formatted_leaders}', content, flags=re.DOTALL)
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  - Added {len(additional_names)} new names")
    print(f"  - Total leader names: {len(all_names)}")
    print(f"  - New names: {', '.join(additional_names)}")

def main():
    """Main function to process all country files."""
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    countries_dir = os.path.join(root_dir, 'common', 'countries')
    first_names_file = os.path.join(script_dir, 'example_leaders_firstnames.txt')
    surnames_file = os.path.join(script_dir, 'example_leaders_surnames.txt')
    
    # Check if directories and files exist
    if not os.path.exists(countries_dir):
        print(f"Error: Countries directory not found at {countries_dir}")
        return
    
    if not os.path.exists(first_names_file):
        print(f"Error: First names file not found at {first_names_file}")
        return
    
    if not os.path.exists(surnames_file):
        print(f"Error: Surnames file not found at {surnames_file}")
        return
    
    # Load name lists
    print("Loading name lists...")
    first_names = load_names_from_file(first_names_file)
    surnames = load_names_from_file(surnames_file)
    
    if not first_names or not surnames:
        print("Error: Could not load name lists")
        return
    
    print(f"Loaded {len(first_names)} first names and {len(surnames)} surnames")
    
    # Get all .txt files in the countries directory
    country_files = [f for f in os.listdir(countries_dir) if f.endswith('.txt')]
    print(f"\nFound {len(country_files)} country files to process")
    
    # Process each country file
    processed_count = 0
    for filename in country_files:
        file_path = os.path.join(countries_dir, filename)
        try:
            process_country_file(file_path, first_names, surnames)
            processed_count += 1
            print()  # Add blank line between files
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"Completed! Processed {processed_count} out of {len(country_files)} files.")

if __name__ == "__main__":
    main()
