import requests

def search_wikipedia(category):
    """
    Search Wikipedia for pages in a specific category.

    :param category: The main category to search (e.g., 'Technology and applied sciences').
    :return: A list of page titles.
    """
    # Endpoint for the Wikipedia API
    url = "https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "max"
    }

    # Make the request to the API
    response = requests.get(url, params=params)
    
    # Check for a valid response
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    data = response.json()

    # Extract page titles from the response
    if "query" in data and "categorymembers" in data["query"]:
        return [item["title"] for item in data["query"]["categorymembers"]]
    else:
        print("Error: No data found in the response")
        return []

# Load categories from an external file
if __name__ == "__main__":
    try:
        with open("categories.txt", "r") as file:
            categories = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: 'categories.txt' file not found.")
        categories = []

    for category in categories:
        print("=" * len(f"Category: {category}"))
        print(f"Category: {category}")
        print("=" * len(f"Category: {category}"))
        results = search_wikipedia(category)
        for title in results:
            print(title)
        print()

