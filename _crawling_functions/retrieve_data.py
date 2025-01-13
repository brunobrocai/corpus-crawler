import json
import os
import csv
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def urls_from_files(directory):
    """
    Read all .html files in a directory and extract the first line of each.

    The first lines are assumed to be URLs.

    Args:
        directory (str): The directory to read the .html files from.

    Returns:
        set: A set of URLs extracted from the first line of each .html file.
    """

    url_set = set()
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            with open(
                f'{directory}/{filename}',
                'r', encoding='utf-8'
            ) as file:
                first_line = file.readline().strip()
                url_set.add(first_line)
    return url_set


def get_imgs_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            dict_ = json.load(file)
        html = dict_['html_content']
        soup = BeautifulSoup(html, 'html.parser')

        img_urls = set()
        for tag in soup.find_all('img', src=True):
            absolute_url = tag['src']
            img_urls.add(absolute_url)

        return img_urls

    except Exception as e:
        print(f"Error: {e}")
        return set()


def get_imgs_from_file(file_path):
    """
    Extract all unique image URLs from the HTML content in a file.

    The function reads the file, parses the HTML content using BeautifulSoup,
    finds all img-tags with a 'src' attribute, and adds the value of this
    attribute to a set. If an error occurs during this process, an error
    message is printed and an empty set is returned.

    Args:
        file_path (str): The path to the file containing the HTML content to
                         extract image URLs from.

    Returns:
        set: A set of unique image URLs found in the HTML content, or an empty
             set if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html = file.read()

        html = html.split('#####')[1]

        soup = BeautifulSoup(html, 'html.parser')

        img_urls = set()
        for tag in soup.find_all('img', src=True):
            absolute_url = tag['src']
            img_urls.add(absolute_url)

        return img_urls

    except Exception as e:
        print(f"Error: {e}")
        return set()


def get_links_from_file(file_path):
    """
    Extract all unique links from the HTML content in a file.

    The function reads the file, parses the HTML content using BeautifulSoup,
    finds all a-tags and link-tags with a 'href' attribute, and adds the value
    of this attribute to a set. If an error occurs during this process, an
    error message is printed and an empty set is returned.

    Args:
        file_path (str): The path to the file containing the HTML content to
                         extract links from.

    Returns:
        set: A set of unique links found in the HTML content, or an empty set
             if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        soup = BeautifulSoup(data['html_content'], 'lxml')

        links = set()
        for tag in soup.find_all(['a', 'link'], href=True):
            absolute_url = tag['href']
            links.add(absolute_url)

        return links

    except Exception as e:
        print(f"Error: {e}")
        return set()


def read_linklist(filepath):
    """
    Read a file and split its content by newline characters.

    The resulting lines, after removing any empty lines, are returned.

    Args:
        filepath (str): The path to the file to read.

    Returns:
        set: A set of lines from the file.
    """

    with open(filepath, 'r', encoding='utf-8') as file:
        links = file.readlines()
    links = {link.rstrip() for link in links if link.strip()}
    return set(links)


def get_html_from_url(url):
    """
    Retrieve the HTML content from a given URL.

    The function sends a GET request to the provided URL and returns the text
    content of the response. If the request fails for any reason, an error
    message is printed and None is returned.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Returns:
        str: The text content of the response, or None if the request fails.
    """

    response = requests.get(
        url,
        timeout=20
    )
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.text


def get_content_from_url(url):
    """
    Retrieve the HTML content from a given URL.

    The function sends a GET request to the provided URL and returns the text
    content of the response. If the request fails for any reason, an error
    message is printed and None is returned.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Returns:
        str: The text content of the response, or None if the request fails.
    """

    response = requests.get(
        url,
        timeout=20
    )
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.content


def get_links_from_html(html):
    """
    Extract all unique links from the provided HTML content.

    The function parses the HTML content using BeautifulSoup, finds all a-tags
    with a 'href' attribute, and adds the value of this attribute to a set. If
    an error occurs during this process, an error message is printed and an
    empty set is returned.

    Args:
        html (str): The HTML content to extract links from.

    Returns:
        set: A set of unique links found in the HTML content, or an empty set
             if an error occurs.
    """
    try:
        soup = BeautifulSoup(html, 'lxml')

        links = set()
        for a_tag in soup.find_all(['a', 'link'], href=True):
            absolute_url = a_tag['href']
            links.add(absolute_url)

        return links

    except Exception as e:
        print(f"Error: {e}")
        return set()


def get_links_from_netdoktor_html(html):

    soup = BeautifulSoup(html, 'html.parser')
    # Find all script tags with type "application/ld+json"
    script_tags = soup.find_all("a", href=True)
    for tag in script_tags:
        absolute_url = tag['href']
        print(absolute_url)

    return set()


def links_from_corpus(corpus_dir):
    """
    Extract links from all HTML files in a given directory.

    The function iterates over all files in the provided directory. If a file
    ends with '.html', it is opened and its content is read. The HTML content
    is split at the first occurrence of '#####', and the second part is used to
    extract links. The extracted links are added to a set.

    If no HTML files are found in the directory, an empty set is returned.

    Args:
        corpus_dir (str): The directory to search for HTML files.

    Returns:
        set: A set of links extracted from all HTML files found
            in the directory, or an empty set if no HTML files are found.
    """
    html_files = [
        os.path.join(corpus_dir, f) for f in os.listdir(corpus_dir)
        if f.endswith('.json')
    ]

    links = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(get_links_from_file, f): f for f in html_files
        }
        for future in tqdm(
            concurrent.futures.as_completed(future_to_file),
            total=len(future_to_file),
            desc="Processing HTML files"
        ):
            links.update(future.result())

    return links


def imgs_from_corpus(corpus_dir):
    """
    Extract images from all HTML files in a given directory.

    The function iterates over all files in the provided directory. If a file
    ends with '.html', it is opened and its content is read. The HTML content
    is split at the first occurrence of '#####', and the second part is used to
    extract images. The extracted images are added to a set.

    If no HTML files are found in the directory, an empty set is returned.

    Args:
        corpus_dir (str): The directory to search for HTML files.

    Returns:
        set: A set of images extracted from all HTML files found
            in the directory, or an empty set if no HTML files are found.
    """
    html_files = [
        os.path.join(corpus_dir, f) for f in os.listdir(corpus_dir)
        if f.endswith('.html')
    ]

    imgs = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(get_imgs_from_file, f): f for f in html_files
        }
        for future in tqdm(
            concurrent.futures.as_completed(future_to_file),
            total=len(future_to_file),
            desc="Processing HTML files"
        ):
            imgs.update(future.result())

    return imgs


def imgs_from_jsoncorpus(corpus_dir):
    """
    Extract images from all HTML files in a given directory.

    The function iterates over all files in the provided directory. If a file
    ends with '.html', it is opened and its content is read. The HTML content
    is split at the first occurrence of '#####', and the second part is used to
    extract images. The extracted images are added to a set.

    If no HTML files are found in the directory, an empty set is returned.

    Args:
        corpus_dir (str): The directory to search for HTML files.

    Returns:
        set: A set of images extracted from all HTML files found
            in the directory, or an empty set if no HTML files are found.
    """
    html_files = [
        os.path.join(corpus_dir, f) for f in os.listdir(corpus_dir)
        if f.endswith('.json')
    ]

    imgs = set()

    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        future_to_file = {
            executor.submit(get_imgs_from_json, f): f for f in html_files
        }
        for future in tqdm(
            concurrent.futures.as_completed(future_to_file),
            total=len(future_to_file),
            desc="Processing json files"
        ):
            imgs.update(future.result())

    return imgs


def list_urls_from_files(directory):
    url_set = set()
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            with open(
                f'{directory}/{filename}',
                'r', encoding='utf-8'
            ) as file:
                first_line = file.readline().strip()
                url_set.add(first_line)
    return url_set


def urls_from_jsons(directory):
    url_set = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(
                f'{directory}/{filename}',
                'r', encoding='utf-8'
            ) as file:
                data = json.load(file)
                url_set.add(data['url'])
    return url_set


def read_index_csv(file_path):
    crawled = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                crawled.add(row[0])
    return crawled


def get_content_from_url(url, selector='body', timeout=300):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Go to the URL
            page.goto(url)

            # Wait for the content to be rendered
            page.wait_for_selector(selector, timeout=timeout)

            # Extract the HTML content
            html_content = page.content()

            # Close the browser
            browser.close()

            print('heheh')

            return html_content
    except PlaywrightTimeoutError:
        print(f"Timeout waiting for {selector} on {url}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
