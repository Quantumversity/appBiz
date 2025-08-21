import os
import requests
from bs4 import BeautifulSoup
import re

class UrlCrawler:
    def __init__(self):
        self.url = None
        self.content = None
        self.clean_text = None

    def fetch_url(self, url):
        """Fetch content from the given URL"""
        try:
            self.url = url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.content = response.text
            print(f"fetched content: {self.content[:100]}...")  # Print the first 100 characters
            return True
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return False

    def clean_content(self):
        """Remove CSS, JS"""
        if not self.content:
            return False

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(self.content, 'html.parser')
        print("1")

        # Remove unwanted elements except h1, h2, h3
        for element in soup(['head', 'style', 'script', 'meta', 'link']):
            element.decompose()
        print("2")


        # Replace heading tags with markers
        for tag in ['h1', 'h2', 'h3']:
            for element in soup.find_all(tag):
                # Preserve the heading tags
                element.insert_before(f'<{tag}>')
                element.insert_after(f'</{tag}>')
                # Replace the original tag with its text
                element.unwrap()

        print("3")

        # Get text content
        text = soup.get_text()
        
        # Clean up the text while preserving heading tags
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if line:
                if any(tag in line for tag in ['<h1>', '<h2>', '<h3>', '</h1>', '</h2>', '</h3>']):
                    lines.append(line)
                else:
                    chunks = [phrase.strip() for phrase in line.split("  ")]
                    lines.extend(chunk for chunk in chunks if chunk)
        
        self.clean_text = '\n'.join(lines)
        return True

    def get_text(self, url):
        """Main method to fetch and clean URL content"""
        if self.fetch_url(url) and self.clean_content():
            return self.clean_text
        return None

def main():
    crawler = UrlCrawler()
    url = input("Enter the URL to crawl: ").strip()

    # create out folder, if not exist
    out_folder = "out"
    os.makedirs(out_folder, exist_ok=True)

    # output filename based on URL
    # if url starts with http:// or https://, remove it
    output_filename = re.sub(r'^https?://', '', url)
    # remove everything after the first /
    output_filename = re.sub(r'/.*$', '', output_filename)
    output_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', output_filename) + ".txt"
    output_filename = os.path.join(out_folder, output_filename)

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            text = crawler.get_text(url)
            if text:
                f.write("Cleaned text content:\n")
                f.write("-" * 50 + "\n")
                f.write(text)
                print(f"\nContent has been written to {output_filename}")
            else:
                f.write("Failed to retrieve and clean the content.")
                print(f"\nError message has been written to {output_filename}")
    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}")

if __name__ == "__main__":
    main()
