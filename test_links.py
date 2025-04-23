import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import test_config


def get_test_links(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    test_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        # Ignore mailto links
        if href is not None and not href.startswith('mailto'):
            test_links.append(href)
    return test_links


def get_base_url():
    # Get base URL from config
    return test_config.baseURLs[test_config.ENVIRONMENT]


def test_home_page_links():
    base_path = get_base_url()
    test_page_url = base_path
    print(f"Testing home page links at {test_page_url}")
    test_links = get_test_links(test_page_url)
    for link in test_links:
        url = urljoin(base_path, link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code in [
            200, 999], f"Link {link} is broken"


def test_about_page_links():
    base_path = get_base_url()
    test_page_url = urljoin(base_path, '/about/about.html')
    print(f"Testing about page links at {test_page_url}")
    test_links = get_test_links(test_page_url)
    for link in test_links:
        url = urljoin(base_path, link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code in [
            200, 999], f"Link {link} is broken"


def test_writing_page_links():
    writing_path = '/writing/writing.html'
    base_path = get_base_url() + writing_path
    test_page_url = urljoin(base_path, writing_path)
    print(f"Testing writing page links at {test_page_url}")
    test_links = get_test_links(test_page_url)
    for link in test_links:
        url = urljoin(base_path, link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code in [200, 999], f"Link {link} is broken"


def test_projects_page_links():
    projects_path = '/projects/projects.html'
    base_path = get_base_url() + projects_path
    test_page_url = urljoin(base_path, projects_path)
    print(f"Testing projects page links at {test_page_url}")
    test_links = get_test_links(test_page_url)
    for link in test_links:
        url = urljoin(base_path, link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code in [200, 999], f"Link {link} is broken"


def test_descriptify_home_page_links():
    descriptify_path = '/projects/descriptify/descriptify.html'
    base_path = get_base_url() + descriptify_path
    test_page_url = urljoin(base_path, descriptify_path)
    print(f"Testing descriptify home page links at {test_page_url}")
    test_links = get_test_links(test_page_url)
    for link in test_links:
        url = urljoin(base_path, link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        assert response.status_code in [200, 999], f"Link {link} is broken"
