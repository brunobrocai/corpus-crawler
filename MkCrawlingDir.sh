#!/bin/bash

# Check if the user provided an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_name>"
    exit 1
fi

# Create the directories
mkdir "$1"
mkdir "$1"/nonarticle_pages
mkdir "$1"/article_pages
mkdir "$1"/resources

touch "$1"/resources/visited.txt
touch "$1"/resources/error.txt
touch "$1"/resources/graph.txt
touch "$1"/resources/queue.txt
touch "$1"/resources/irrelevant.txt
touch "$1"/resources/forbidden.txt


# Check if the directory creation was successful
if [ $? -eq 0 ]; then
    echo "Directory '$1' created or updated successfully."
else
    echo "Failed to create directory '$1'."
fi
