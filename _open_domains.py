import os


def list_dirs(directory):
    """
    List all directories in a given directory.

    Args:
        directory (str): The directory to search for subdirectories.

    Returns:
        list: A list of all subdirectories found in the provided directory.
    """
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f))
    ]


if __name__ == '__main__':
    current_dirs = list_dirs('.')
    for direc in current_dirs:
        graph_path = os.path.join(direc, 'resources', 'graph.txt')

        try:
            with open(graph_path, 'r', encoding='utf-8') as file:
                try:
                    last_line = file.readlines()[-1]
                    if int(last_line) > 0:
                        print(f'{direc}: {last_line}')
                except IndexError as e:
                    print(f'{e} in {direc}')
        except FileNotFoundError:
            pass
