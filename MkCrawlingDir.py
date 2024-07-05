import os
import sys


def create_directory(dir_name):
    if not dir_name:
        raise ValueError("Directory name cannot be empty.")

    os.makedirs(os.path.join(dir_name, "nonarticle_pages"), exist_ok=True)
    os.makedirs(os.path.join(dir_name, "article_pages"), exist_ok=True)
    os.makedirs(os.path.join(dir_name, "resources"), exist_ok=True)

    open(os.path.join(dir_name, "resources", "visited.txt"), 'a').close()
    open(os.path.join(dir_name, "resources", "error.txt"), 'a').close()
    open(os.path.join(dir_name, "resources", "graph.txt"), 'a').close()
    open(os.path.join(dir_name, "resources", "queue.txt"), 'a').close()
    open(os.path.join(dir_name, "resources", "irrelevant.txt"), 'a').close()
    open(os.path.join(dir_name, "resources", "forbidden.txt"), 'a').close()


dir_name = sys.argv[1]
create_directory(dir_name)

print(f'Directory {dir_name} created or updated successfully.')
