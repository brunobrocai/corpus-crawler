import os
import sys


def count_files(directory):
    file_count = 0

    if not os.path.exists(directory):
        raise FileNotFoundError(f'Directory {directory} not found.')

    for _, _, files in os.walk(directory):
        file_count += len(files)
    return file_count


try:
    site = sys.argv[1]
    if site[-1] != '/':
        site += '/'
except IndexError:
    print('Please provide a site name as an argument.')
    sys.exit(1)

try:
    article_files = count_files(f'{site}page_contents')
    board_files = count_files(f'{site}board_pages')

except FileNotFoundError:
    article_files = count_files(f'{site}article_pages')
    board_files = count_files(f'{site}nonarticle_pages')

print(f'article files: {article_files}')
print(f'Board files: {board_files}')
