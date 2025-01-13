# Corpus Crawler
This is a python command line tool that lets you crawl a website and download html that is relevant to you.

## Requirements
Before executing, make sure you have the following python libraries installed:

+ bs4
+ requests
+ tqdm
+ lxml
+ typer

You can install them by running the following command:
```bash
pip install bs4 requests tqdm lxml typer
```

In addition, you need `playwright` to be installed. Check the playwright documentation for the installation instructions. It can be found [here](https://playwright.dev/python/docs/intro).

## Usage
This tool runs on the command line. To crawl a site, perform the following steps:

### Create directory
Create a new directory to store the crawled data. This is performed by the *MkCrawlingDir.sh* script.
```bash
./MkCrawlingDir.sh <dir_name>
```

### Add Website Pattern
In the patterns.ini file, add data about the webiste you want to crawl. The file is structured as follows:

```python
[<dir_name>]  # The name of the directory from before

base_url = <base_url>  # The base url of the website. Do NOT add a trailing slash!

article_url = <article_url>  # The url regex pattern of the articles.

not_article_url = <not_article_url>  # The url regex pattern of the pages that are not articles, but you nevertheless want to crawl. These can be e.g. the homepage, the about page, etc.

irrelevant_urls = <irrelevant_url>  # If a url contains this regex pattern, it will be ignored.
```

### (Optional) Create a checker function
If you want to check if a page is relevant before downloading it, you can create a function in the *_checker_funcs.py* file. The function should have the following signature:

```python
def check(html: str, url: str) -> bool:
    # Your code here

    # Return True if the page is relevant,
    # False to skip it
    return True
```

### (Optional) Add urls to the queue
If you have a starting point you want, you can manually add urls to the queue. To do this, add lines with urls you want to crawl to the queue.txt file in the <dir_name>/resources/ directory.

If you want to automatically add a list of urls as your starting point, you can define a function that generates such links in the *_generations_funcs.py* file. This can be useful e.g. if you have a set of urls that only differ in the page number that you want to crawl. The function should have the following signature:

```python
def generate(amount: int, dirname: str) -> None:
    # Your code here

    # The urls will be written into the queue of the specified dir
```

or

```python
def generate(amount: int, dirname: str, special_param: str) -> None:
    # Your code here

    # The urls will be written into the queue of the specified dir
```

To generate the urls to the queue, run the following command. It takes the following args:
+ dir_name: The name of the directory from before
+ function: The name of the function you defined above
+ amount: The amount of links you want to add (e.g. 100 if the website has 100 pages)
+ special_param: A special parameter that you might need for your function (optional). This usually is the base url of the domain (e.g. topic page) that you want to crawl.

```bash
python generate_links.py <dir_name> <function> <amount> <special_param>
```


### Run the crawler
There are two crawlers available, depending on wether or not you want to use a checker function. To run the crawler, execute the following command:

```bash
python crawl.py <dir_name> <options>
```

There are two options at the moment:
>`--checker (or -c) <checker_function_name>`
>
>Run a check before declaring a page as relevant. The function should be defined in the *_checker_funcs.py* file. Pass its name with the option `-c`.

>`--dynamic (or -d)`
>
>Use the dynamic crawler. This crawler uses the playwright library to crawl the website. This is useful if the website uses javascript to load the content. The dynamic crawler is slower than the static one and not necessary if the website does not place important content behind javascript.

Here is an example using both options:
```bash
python crawl.py <dir_name> --checker <checker_function_name> --dynamic
```


## Monitoring and Post-Editing
You can keep track of your crawling with the three python files starting with a \_:

### \_build_graph.py
... creates a graph that shows how many pages were still open at any point in your crawling.

Requirements:
+ numpy
+ matplotlib

Run the following command install the required libraries:
```bash
pip install numpy matplotlib
```

Usage:
```bash
python _build_graph.py <dir_name>
```

### \_corpus_metadata.py
Find out how many files you have crawled.

Usage:
```bash
python _corpus_metadata.py <dir_name>
```

### \_open_domains.py
Find out how many domains and how many urls from those domains are still left to crawl.

Usage:
```bash
python _open_domains.py
```
