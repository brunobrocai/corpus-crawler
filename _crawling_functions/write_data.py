import os
import json
import datetime


def dump_html(folder, filename, html):
    """
    Write HTML content to a file.

    All slashes in the filename are replaced with underscores. The file is
    saved in the specified folder with a '.html' extension.
    At the top of the file, the URL is written as the first line.

    Args:
        folder (str): The folder where the file is to be saved.
        filename (str): The name of the file.
        html (str): The HTML content to write to the file.
    """

    filename = filename.replace('/', '_')
    filename = filename[:250]
    file_path = f'{folder}/{filename}.html'

    if os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' already exists.")

    with open(file_path, 'w', encoding='utf-8') as output:
        output.write(html)


def write_html_to_json(folder, url, html):
    """
    Write HTML content to a file in JSON format.

    All slashes in the filename are replaced with underscores. The file is
    saved in the specified folder with a '.json' extension.
    At the top of the file, the URL is written as the first line.

    Args:
        folder (str): The folder where the file is to be saved.
        filename (str): The name of the file.
        html (str): The HTML content to write to the file.
    """

    filename = url.replace('/', '_')
    filename = filename[:250]
    file_path = f'{folder}/{filename}.json'

    if os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' already exists.")

    data = {
            'url': url,
            'time_crawled': str(datetime.datetime.now().isoformat()),
            'html_content': html
        }

    with open(file_path, 'w', encoding='utf-8') as output:
        json.dump(data, output)


def append_line_to_file(file_path, new_line):
    """Does what it says."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(new_line + '\n')


def append_lines_to_file(file_path, new_lines):
    """Does what it says."""
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in new_lines:
            file.write(line + '\n')


def write_lines_to_file(file_path, lines, newline=True):
    """Does what it says."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if newline:
                file.write(line + '\n')
            else:
                file.write(line)


def write_uniques(filepath, verbose=False):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    line_set = set(lines)
    write_lines_to_file(filepath, line_set, newline=False)

    if verbose:
        print(
            f'Wrote {len(line_set)} unique lines'
            f'from {len(lines)} total lines.')


def save_indexed_media(binary, folder, number, extension):
    file_path = f'{folder}/{number}.{extension}'

    if os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' already exists.")

    with open(file_path, 'wb') as file:
        file.write(binary)
