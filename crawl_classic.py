import sys
from _crawling_functions import new_crawlers


def handle_cmd_line_args():
    """Handle the command line arguments.

    Returns:
        str: The path to the configuration file.
    """
    if len(sys.argv) < 2:
        print('Usage: python crawl_classic.py <site to crawl>')
        sys.exit(1)

    sitename = sys.argv[1]
    if sitename.endswith('/'):
        sitename = sitename[:-1]

    return sitename


SITENAME = handle_cmd_line_args()

NewCrawler = new_crawlers.ClassicCrawler(
    SITENAME
)

NewCrawler.start_crawling()
