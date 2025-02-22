from . import write_data


def generate_spektrum_links(pages, dir_path, base_url):
    link_set = set()
    for i in range(1, pages+1):
        link_set.add(f'{base_url}?skip={str((i-1)*10)}')
    write_data.append_lines_to_file(
        f'{dir_path}',
        link_set
    )


def generate_zeit_links(pages, dirpath, base_url):
    link_set = set()
    link_set.add(base_url)
    for i in range(2, pages+1):
        link_set.add(f'{base_url}&p={str(i)}')
    write_data.write_lines_to_file(dirpath, link_set)
