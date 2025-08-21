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
            print(f"fetched content: {self.content[:200]}...")  # Print the first 100 characters
            self.write_to_file("out/fetched_content.txt", self.content)
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
        print("4, text=", text[:100])

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

        print("5")
        self.clean_text = '\n'.join(lines)
        print("6, cleaned text:", self.clean_text[:100])
        return True

    def get_text(self, url):
        """Main method to fetch and clean URL content"""
        if self.fetch_url(url) and self.clean_content():
            print("Content fetched and cleaned successfully.")
            return self.clean_text
        return None

    def write_to_file(self, file_path, text):
        """Write the cleaned text to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Content has been written to {file_path}")
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")

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
    
    text = crawler.get_text(url)
    crawler.write_to_file(output_filename, text)

if __name__ == "__main__":
    main()
