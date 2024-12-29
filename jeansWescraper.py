#jean choe 2024 december
import requests
from bs4 import BeautifulSoup

def web_scraper(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extract all the links from the webpage
        links = []
        for a_tag in soup.find_all('a', href=True):
            links.append(a_tag['href'])

        return links

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Replace input() with a hardcoded URL for non-interactive environments
    url = "https://example.com"  # Replace with the desired URL
    scraped_links = web_scraper(url)
    print("\nScraped Links:")
    for link in scraped_links:
        print(link)
