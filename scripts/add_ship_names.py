#!/usr/bin/env python3
"""
Script to add 15 random ship names to all EU4 country files.
Combines adjectives and nouns with specified probability distribution:
- 60% chance: "ADJECTIVE NOUN"
- 40% chance: "NOUN ADJECTIVE"
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

def generate_ship_name(adjectives, nouns):
    """Generate a ship name with 60% chance ADJECTIVE NOUN, 40% chance NOUN ADJECTIVE."""
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    
    # 60% chance for "ADJECTIVE NOUN", 40% chance for "NOUN ADJECTIVE"
    if random.random() < 0.6:
        return f"{adjective} {noun}"
    else:
        return f"{noun} {adjective}"

def generate_unique_ship_names(adjectives, nouns, count=15):
    """Generate a list of unique ship names."""
    ship_names = set()
    attempts = 0
    max_attempts = 1000  # Prevent infinite loop
    
    while len(ship_names) < count and attempts < max_attempts:
        new_name = generate_ship_name(adjectives, nouns)
        ship_names.add(new_name)
        attempts += 1
    
    return list(ship_names)

def format_ship_names(names):
    """Format ship names for the ship_names section."""
    formatted_names = '\n'.join([f'\t"{name}"' for name in names])
    return f"{{\n{formatted_names}\n}}"

def get_existing_ship_names(content):
    """Extract existing ship names from country file content."""
    # Find the ship_names section
    ship_match = re.search(r'ship_names\s*=\s*\{([^}]*)\}', content, re.DOTALL)
    if ship_match:
        ship_content = ship_match.group(1)
        # Extract quoted names
        names = re.findall(r'"([^"]+)"', ship_content)
        return names
    return []

def process_country_file(file_path, adjectives, nouns):
    """Process a single country file to add ship names."""
    print(f"Processing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get existing ship names
    existing_ships = get_existing_ship_names(content)
    print(f"  - Current ship names: {len(existing_ships)}")
    
    # Generate 15 unique ship names
    new_ship_names = generate_unique_ship_names(adjectives, nouns, 15)
    
    # Format the ship names
    formatted_ships = format_ship_names(new_ship_names)
    
    # Replace the ship_names section
    content = re.sub(r'ship_names\s*=\s*\{[^}]*\}', f'ship_names = {formatted_ships}', content, flags=re.DOTALL)
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  - Added {len(new_ship_names)} ship names")
    print(f"  - Sample names: {', '.join(new_ship_names[:5])}...")

def main():
    """Main function to process all country files."""
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    countries_dir = os.path.join(root_dir, 'common', 'countries')
    nouns_file = os.path.join(script_dir, 'ship_names_nouns.txt')
    adjectives_file = os.path.join(script_dir, 'ship_names_adjectives.txt')
    
    # Check if directories and files exist
    if not os.path.exists(countries_dir):
        print(f"Error: Countries directory not found at {countries_dir}")
        return
    
    if not os.path.exists(nouns_file):
        print(f"Error: Nouns file not found at {nouns_file}")
        return
    
    if not os.path.exists(adjectives_file):
        print(f"Error: Adjectives file not found at {adjectives_file}")
        return
    
    # Load word lists
    print("Loading word lists...")
    nouns = load_names_from_file(nouns_file)
    adjectives = load_names_from_file(adjectives_file)
    
    if not nouns or not adjectives:
        print("Error: Could not load word lists")
        return
    
    print(f"Loaded {len(nouns)} nouns and {len(adjectives)} adjectives")
    
    # Get all .txt files in the countries directory
    country_files = [f for f in os.listdir(countries_dir) if f.endswith('.txt')]
    print(f"\nFound {len(country_files)} country files to process")
    print("Ship name format: 60% 'ADJECTIVE NOUN', 40% 'NOUN ADJECTIVE'")
    
    # Process each country file
    processed_count = 0
    for filename in country_files:
        file_path = os.path.join(countries_dir, filename)
        try:
            process_country_file(file_path, adjectives, nouns)
            processed_count += 1
            print()  # Add blank line between files
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"Completed! Processed {processed_count} out of {len(country_files)} files.")

if __name__ == "__main__":
    main()
