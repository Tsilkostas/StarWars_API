import requests

SWAPI_BASE = "https://swapi.info/api"

def fetch_all(resource: str):
    """
    Fetches all items of a given resource type from SWAPI, handling pagination.

    Args:
        resource (str): The SWAPI resource to fetch.
            - Use 'people' for Star Wars characters (SWAPI uses 'people', not 'characters')
            - Use 'films' for films
            - Use 'starships' for starships

    Returns:
        list: A list of dictionaries, each representing a resource item from SWAPI.

    Raises:
        requests.HTTPError: If the SWAPI request fails.
    """
    results = []
    url = f"{SWAPI_BASE}/{resource}/"
    while url:
        resp = requests.get(url, timeout=10) # Make a GET request to the current page
        resp.raise_for_status() # Make a GET request to the current page
        data = resp.json()  # Parse JSON response
        results.extend(data.get("results", [])) # Add results from this page
        url = data.get("next") # Get the next page URL, if any
    return results

def parse_swapi_id(url: str) -> int:
    """
    Extracts the numeric SWAPI ID from a SWAPI resource URL.

    Args:
        url (str): The SWAPI resource URL (e.g., 'https://swapi.info/api/people/1/').

    Returns:
        int: The extracted SWAPI ID, or -1 if extraction fails.
    """
    try:
        return int(url.strip("/").split("/")[-1]) # Get the last part of the URL and convert to int
    except Exception:
        return -1 # Return -1 if parsing fails