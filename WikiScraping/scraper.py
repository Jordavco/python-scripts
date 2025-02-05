import requests
import html
import textwrap

class WikipediaFetcher:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/w/api.php"
        self.session = requests.Session()
    
    def get_page_content(self, title):
        
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "exintro": False
        }
        
        try:
            response = self.session.get(url=self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract page data
            pages = data["query"]["pages"]
            page_id = list(pages.keys())[0]
            
            if page_id == "-1":
                return None, None, False
                
            page_data = pages[page_id]
            return page_data["title"], page_data["extract"], True
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return None, None, False
        except (KeyError, IndexError) as e:
            print(f"Error parsing response: {e}")
            return None, None, False
    
    def search_wikipedia(self, query, limit=5):
        """
        Search Wikipedia for pages matching the query.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results to return
            
        Returns:
            list: List of search results
        """
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": limit
        }
        
        try:
            response = self.session.get(url=self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data["query"]["search"]
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    def get_random_article(self):
        """Get a random article from Wikipedia."""

        params = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnlimit": 1,
            "rnnamespace": 0,
            "prop": "extracts",
            "explaintext": True,
            "exintro": False
        }
        try:
            response = self.session.get(url=self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            print(data["query"]["random"][0]["title"])
            return self.get_page_content(data["query"]["random"][0]["title"])
        except Exception as e:
            print(f"Error getting random article: {e}")
            return None, None, False

def display_content(title, content, width=80):
    """Format and display the Wikipedia content."""
    if title and content:
        print("\n" + "=" * width)
        print(f"{title.center(width)}")
        print("=" * width + "\n")
        
        # Wrap text to specified width
        wrapped_content = textwrap.fill(content, width=width)
        print(wrapped_content + "\n")
    else:
        print("No content found.")



def main():
    wiki = WikipediaFetcher()
    
    while True:
        print("\nWikipedia Content Fetcher")
        print("1. Search for a page")
        print("2. Get page by exact title")
        print("3. Get random article")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            query = input("Enter search query: ")
            results = wiki.search_wikipedia(query)
            
            if results:
                print("\nSearch results:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['title']}")
                
                selection = input("\nEnter number to view content (or press Enter to skip): ")
                if selection.isdigit() and 1 <= int(selection) <= len(results):
                    title, content, success = wiki.get_page_content(results[int(selection)-1]['title'])
                    display_content(title, content)
            else:
                print("No results found.")
                
        elif choice == "2":
            title = input("Enter exact page title: ")
            title, content, success = wiki.get_page_content(title)
            display_content(title, content)
        
        elif choice == "3":
            title, content, success = wiki.get_random_article()
            display_content(title, content)
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()