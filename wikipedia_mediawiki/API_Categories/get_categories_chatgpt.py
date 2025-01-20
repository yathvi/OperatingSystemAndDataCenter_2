#!/usr/bin/python3

"""
    get_categories.py

    MediaWiki API Demos
    Fetch and display categories associated with multiple Wikipedia pages,
    excluding categories containing specific keywords (case insensitive).

    MIT License
"""

import requests

def get_categories(page_titles):
    """
    Fetch and print categories associated with given Wikipedia page titles,
    excluding categories containing specific keywords (case insensitive).

    Args:
        page_titles (list): List of Wikipedia page titles.
    """
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    # Updated keywords to exclude (case-insensitive)
    exclude_keywords = [
        "articles", 
        "cs1", 
        "short description", 
        "dmy dates", 
        "mdy dates", 
        "webarchive", 
        "pages using", 
        "disputes", 
        "commons category", 
        "commons link", 
        "cleanup", 
        "wikipedia"
    ]

    for page_title in page_titles:
        PARAMS = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "cllimit": "500",
            "titles": page_title
        }

        try:
            R = S.get(url=URL, params=PARAMS)
            R.raise_for_status()
            DATA = R.json()

            PAGES = DATA.get("query", {}).get("pages", {})

            header = f"Categories for page '{page_title}':"
            print(header)
            print("-" * len(header))  # Underline with dashes

            for k, v in PAGES.items():
                if "categories" in v:
                    has_categories = False
                    for cat in v['categories']:
                        # Exclude categories containing any keyword from the list (case-insensitive)
                        if not any(exclude in cat["title"].lower() for exclude in exclude_keywords):
                            print(cat["title"])
                            has_categories = True
                    if not has_categories:
                        print("No matching categories found.")
                else:
                    print("No categories found.")
            print("\n")  # Separate outputs for different pages with a new line

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching categories for '{page_title}': {e}")

def read_page_titles_from_file(filename):
    """
    Read page titles from a text file.

    Args:
        filename (str): Path to the text file containing the page titles.
    
    Returns:
        list: List of page titles read from the file.
    """
    with open(filename, 'r') as file:
        page_titles = [line.strip() for line in file if line.strip()]
    return page_titles

if __name__ == "__main__":
    # Read page titles from file
    page_titles = read_page_titles_from_file('page_titles.txt')
    
    # Fetch and display categories for the page titles
    get_categories(page_titles)

