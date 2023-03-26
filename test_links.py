import requests
from urllib.parse import urljoin

def test_homepage_links():
    links = ['/', 'writing/writing.html', 'projects/projects.html', 'about/about']
    base_url = 'https://anupam.de'
    for link in links:
        url = urljoin(base_url, link)
        response = requests.get(url)
        assert response.status_code == 200, f"Link {link} is broken"

def test_descriptify_links():
    links = ['/', 'descriptify.html', 'articles/articles.html', 'tutorials/tutorials.html']
    base_url = 'https://anupam.de/projects/descriptify/'
    for link in links:
        url = urljoin(base_url, link)
        print (url)
        response = requests.get(url)
        assert response.status_code == 200, f"Link {link} is broken"