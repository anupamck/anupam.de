import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def get_test_links(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    test_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and not href.startswith('mailto'):
            test_links.append(href)
    return test_links

def test_home_page_links():
    base_url = 'https://anupam.de'
    test_page_url = base_url
    test_links = get_test_links(test_page_url)    
    for link in test_links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code in [200, 999], f"Link {link} is broken"

def test_about_page_links():
    base_url = 'https://anupam.de'
    test_page_url = urljoin(base_url, '/about')
    test_links = get_test_links(test_page_url)    
    for link in test_links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code in [200, 999], f"Link {link} is broken"

def test_writing_page_links():
    base_url = 'https://anupam.de/writing'
    test_page_url = urljoin(base_url, '/writing.html')
    test_links = get_test_links(test_page_url)    
    for link in test_links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code in [200, 999], f"Link {link} is broken"

def test_projects_page_links():
    base_url = 'https://anupam.de/projects'
    test_page_url = urljoin(base_url, '/projects.html')
    test_links = get_test_links(test_page_url)    
    for link in test_links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code in [200, 999], f"Link {link} is broken"

def test_descriptify_home_page_links():
    base_url = 'https://anupam.de/projects/descriptify/descriptify.html'
    test_page_url = base_url
    test_links = get_test_links(test_page_url)    
    for link in test_links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code in [200, 999], f"Link {link} is broken"