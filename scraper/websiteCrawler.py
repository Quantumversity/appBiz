import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_sitemap_links(url):
    sitemap_url = urljoin(url, '/sitemap.xml')
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            links = []
            root = ET.fromstring(response.content)
            for elem in root.iter():
                if 'loc' in elem.tag:
                    links.append(elem.text)
            return links
        else:
            return None
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return None

def get_all_links_from_homepage(url):
    links = set()
    links.add(url)
    domain = urlparse(url).netloc
    print(f"get_all_links_from_homepage(), domain={domain}")
    try:
        response = requests.get(url, headers=headers)
        print(f"get_all_links_from_homepage(), response={response}")
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"get_all_links_from_homepage(), soup={soup}")
        for a_tag in soup.find_all('a', href=True):
            print(f"get_all_links_from_homepage(), a_tag={a_tag}")
            link = urljoin(url, a_tag['href'])
            print(f"get_all_links_from_homepage(), link={link}")
            linkdomain = urlparse(link).netloc
            print(f"get_all_links_from_homepage(), linkdomain={linkdomain}")
            if linkdomain == domain:
                links.add(link)
        return list(links)
    except Exception as e:
        print(f"Error fetching homepage links: {e}")
        return []

def get_content_of_links(links):
    combined_content = ""
    for link in links:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract text content from the webpage
                combined_content += soup.get_text(separator='\n')
        except Exception as e:
            print(f"Error fetching content from {link}: {e}")
    return combined_content

def scrape_website(url):
    links = get_sitemap_links(url)
    if links:
        print("Sitemap found, fetching content from sitemap links.")
    else:
        print("Sitemap not found, extracting links from homepage.")
        links = get_all_links_from_homepage(url)
    
    if not links:
        print("No links found to scrape.")
        return None

    content = get_content_of_links(links)
    return content

# Example usage:
url = input("Enter the website URL: ")
content = scrape_website(url)

if content:
    print("Scraping completed. Length of combined content:", len(content))
    # Trim each line of the content before saving
    trimmed_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    
    # Save trimmed content to a file
    with open("scraped_content.txt", "w", encoding="utf-8") as f:
        f.write(trimmed_content)
else:
    print("No content scraped.")