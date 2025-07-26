#!/usr/bin/env python3
"""
Script to assign random RGB colors, revolutionary colors, and leader names to EU4 country files.
Processes all .txt files in the common/countries directory.
"""

import os
import random
import re

def load_leader_names(file_path):
    """Load leader names from the example_leaders.txt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]
    return names

def generate_random_rgb():
    """Generate a random RGB color in the format { R G B }."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"{{ {r} {g} {b} }}"

def generate_random_revolutionary_color():
    """Generate a random revolutionary color with values 0-16."""
    r = random.randint(0, 16)
    g = random.randint(0, 16)
    b = random.randint(0, 16)
    return f"{{ {r} {g} {b} }}"

def get_random_leader_names(leader_names, count=3):
    """Get a random selection of leader names."""
    return random.sample(leader_names, min(count, len(leader_names)))

def format_leader_names(names):
    """Format leader names for the leader_names section."""
    formatted_names = '\n'.join([f'\t"{name}"' for name in names])
    return f"{{\n{formatted_names}\n}}"

def process_country_file(file_path, leader_names):
    """Process a single country file to add colors and leader names."""
    print(f"Processing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate random colors
    rgb_color = generate_random_rgb()
    revolutionary_color = generate_random_revolutionary_color()
    
    # Get random leader names
    random_leaders = get_random_leader_names(leader_names)
    formatted_leaders = format_leader_names(random_leaders)
    
    # Replace color = { }
    content = re.sub(r'color\s*=\s*\{\s*\}', f'color = {rgb_color}', content)
    
    # Replace revolutionary_colors = { }
    content = re.sub(r'revolutionary_colors\s*=\s*\{\s*\}', f'revolutionary_colors = {revolutionary_color}', content)
    
    # Replace leader_names = { }
    content = re.sub(r'leader_names\s*=\s*\{\s*\}', f'leader_names = {formatted_leaders}', content)
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  - Color: {rgb_color}")
    print(f"  - Revolutionary Color: {revolutionary_color}")
    print(f"  - Leader Names: {', '.join(random_leaders)}")

def main():
    """Main function to process all country files."""
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    countries_dir = os.path.join(root_dir, 'common', 'countries')
    leaders_file = os.path.join(script_dir, 'example_leaders.txt')
    
    # Check if directories and files exist
    if not os.path.exists(countries_dir):
        print(f"Error: Countries directory not found at {countries_dir}")
        return
    
    if not os.path.exists(leaders_file):
        print(f"Error: Leaders file not found at {leaders_file}")
        return
    
    # Load leader names
    print("Loading leader names...")
    leader_names = load_leader_names(leaders_file)
    print(f"Loaded {len(leader_names)} leader names")
    
    # Get all .txt files in the countries directory
    country_files = [f for f in os.listdir(countries_dir) if f.endswith('.txt')]
    print(f"\nFound {len(country_files)} country files to process")
    
    # Process each country file
    processed_count = 0
    for filename in country_files:
        file_path = os.path.join(countries_dir, filename)
        try:
            process_country_file(file_path, leader_names)
            processed_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\nCompleted! Processed {processed_count} out of {len(country_files)} files.")

if __name__ == "__main__":
    main()


