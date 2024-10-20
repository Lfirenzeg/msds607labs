# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:21:30 2024

@author: lucho
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
from datetime import datetime  # For adding timestamps

# Function to load skills from CSV and categorize them into case-sensitive and insensitive
def load_skills_from_csv(file_path):
    skills_df = pd.read_csv(file_path)
    skills = skills_df['skill'].tolist()

    # List of case-sensitive skills to avoid issues
    case_sensitive_skills = ["R", "C", "C++", "SQL"]  # Expand this list based on your needs
    case_insensitive_skills = [skill for skill in skills if skill not in case_sensitive_skills]

    return case_sensitive_skills, case_insensitive_skills

# Function to extract skills from a dynamically loaded page
def extract_skills_with_selenium(url, case_sensitive_skills, case_insensitive_skills):
    # Set up Selenium WebDriver (make sure to have the appropriate driver installed)
    driver = webdriver.Chrome()  # Use Chrome WebDriver
    driver.get(url)
    
    # Wait for the page to load (increase sleep time if page takes longer to load)
    time.sleep(5)
    
    # Get all text content of the page
    original_page_text = driver.find_element(By.TAG_NAME, 'body').text  # Original text content
    lowercased_page_text = original_page_text.lower()  # Lowercase version of text content
    
    # Create a list to store matches
    skill_matches = []
    
    # Check for matches from the case-sensitive skill list using original text
    for skill in case_sensitive_skills:
        # Match exactly the standalone word for case-sensitive skills
        pattern = fr'\b{skill}\b'  # Regex pattern to match exact skill name as a standalone word
        if re.search(pattern, original_page_text):
            skill_matches.append(skill)
    
    # Check for matches from the case-insensitive skill list using lowercased text
    for skill in case_insensitive_skills:
        pattern = re.escape(skill.lower())  # Use re.escape to handle special characters
        if re.search(pattern, lowercased_page_text):
            skill_matches.append(skill)
    
    # Close the driver
    driver.quit()
    
    return skill_matches

# Function to save or update CSV with matched skills
def save_results_to_csv(output_file, url, matched_skills):
    # Create a DataFrame with the URL, timestamp, and matched skills
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_data = {
        'URL': [url],
        'Timestamp': [timestamp],
        'Matched_Skills': [', '.join(matched_skills)]  # Join skills as a single string
    }
    result_df = pd.DataFrame(result_data)
    
    # Append to the CSV if it exists, otherwise create a new one
    try:
        # If file exists, append without writing headers
        result_df.to_csv(output_file, mode='a', index=False, header=False)
    except FileNotFoundError:
        # If file doesn't exist, create it and write headers
        result_df.to_csv(output_file, mode='w', index=False, header=True)
    print(f"Results saved to {output_file}")

# Example URL for a job posting (replace with a real job posting URL)
url = "https://www.sampleurl.com"

# Load skills from the csv file
file_path = r"C:\Sample-path\skills.csv"  #replace sample path with location of file with skill dictionary
output_file = r"C:\Sample-path\matched_skills_results.csv" #replace sample path with desired location for csv

case_sensitive_skills, case_insensitive_skills = load_skills_from_csv(file_path)

# Extract skills from the URL using Selenium
matched_skills = extract_skills_with_selenium(url, case_sensitive_skills, case_insensitive_skills)

print("Skills found in job posting:", matched_skills)

# Save the results to a CSV file
save_results_to_csv(output_file, url, matched_skills)