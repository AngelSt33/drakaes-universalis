#!/usr/bin/env python3
"""
Script to add 10 male and 10 female monarch names to all EU4 country files.
Extracts first names from monarch files and adds them with the correct syntax.
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

def extract_first_names(full_names):
    """Extract first names from full names (removes surnames)."""
    first_names = []
    for full_name in full_names:
        # Split by space and take the first part
        parts = full_name.strip().split()
        if parts:
            first_names.append(parts[0])
    return first_names

def get_random_monarch_names(male_first_names, female_first_names, count_each=10):
    """Get random selection of male and female first names."""
    # Ensure we don't have duplicates and have enough names
    unique_male = list(set(male_first_names))
    unique_female = list(set(female_first_names))
    
    male_count = min(count_each, len(unique_male))
    female_count = min(count_each, len(unique_female))
    
    selected_male = random.sample(unique_male, male_count)
    selected_female = random.sample(unique_female, female_count)
    
    return selected_male, selected_female

def format_monarch_names(male_names, female_names):
    """Format monarch names for the monarch_names section."""
    lines = []
    
    # Add male names with +1
    for name in male_names:
        lines.append(f'\t"{name}" = +1')
    
    # Add female names with -1
    for name in female_names:
        lines.append(f'\t"{name}" = -1')
    
    formatted_names = '\n'.join(lines)
    return f"{{\n{formatted_names}\n}}"

def get_existing_monarch_names(content):
    """Extract existing monarch names from country file content."""
    # Find the monarch_names section
    monarch_match = re.search(r'monarch_names\s*=\s*\{([^}]*)\}', content, re.DOTALL)
    if monarch_match:
        monarch_content = monarch_match.group(1)
        # Extract quoted names and their values
        names = re.findall(r'"([^"]+)"\s*=\s*([+-]?\d+)', monarch_content)
        return names
    return []

def process_country_file(file_path, male_first_names, female_first_names):
    """Process a single country file to add monarch names."""
    print(f"Processing: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get existing monarch names
    existing_monarchs = get_existing_monarch_names(content)
    print(f"  - Current monarch names: {len(existing_monarchs)}")
    
    # Generate random monarch names
    selected_male, selected_female = get_random_monarch_names(male_first_names, female_first_names)
    
    # Format the new monarch names
    formatted_monarchs = format_monarch_names(selected_male, selected_female)
    
    # Replace the monarch_names section
    content = re.sub(r'monarch_names\s*=\s*\{[^}]*\}', f'monarch_names = {formatted_monarchs}', content, flags=re.DOTALL)
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  - Added {len(selected_male)} male names: {', '.join(selected_male)}")
    print(f"  - Added {len(selected_female)} female names: {', '.join(selected_female)}")
    print(f"  - Total monarch names: {len(selected_male) + len(selected_female)}")

def main():
    """Main function to process all country files."""
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    countries_dir = os.path.join(root_dir, 'common', 'countries')
    male_monarchs_file = os.path.join(script_dir, 'example_monarch_male.txt')
    female_monarchs_file = os.path.join(script_dir, 'example_monarch_female.txt')
    
    # Check if directories and files exist
    if not os.path.exists(countries_dir):
        print(f"Error: Countries directory not found at {countries_dir}")
        return
    
    if not os.path.exists(male_monarchs_file):
        print(f"Error: Male monarchs file not found at {male_monarchs_file}")
        return
    
    if not os.path.exists(female_monarchs_file):
        print(f"Error: Female monarchs file not found at {female_monarchs_file}")
        return
    
    # Load monarch name lists
    print("Loading monarch name lists...")
    male_full_names = load_names_from_file(male_monarchs_file)
    female_full_names = load_names_from_file(female_monarchs_file)
    
    if not male_full_names or not female_full_names:
        print("Error: Could not load monarch name lists")
        return
    
    # Extract first names only
    male_first_names = extract_first_names(male_full_names)
    female_first_names = extract_first_names(female_full_names)
    
    print(f"Loaded {len(male_first_names)} male first names and {len(female_first_names)} female first names")
    
    # Remove duplicates
    unique_male = list(set(male_first_names))
    unique_female = list(set(female_first_names))
    print(f"Unique names: {len(unique_male)} male, {len(unique_female)} female")
    
    # Get all .txt files in the countries directory
    country_files = [f for f in os.listdir(countries_dir) if f.endswith('.txt')]
    print(f"\nFound {len(country_files)} country files to process")
    
    # Process each country file
    processed_count = 0
    for filename in country_files:
        file_path = os.path.join(countries_dir, filename)
        try:
            process_country_file(file_path, unique_male, unique_female)
            processed_count += 1
            print()  # Add blank line between files
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"Completed! Processed {processed_count} out of {len(country_files)} files.")

if __name__ == "__main__":
    main()
