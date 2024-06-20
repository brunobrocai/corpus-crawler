import sys
from _crawling_functions import new_crawlers, _checker_funcs


def handle_cmd_line_args():
    """Handle the command line arguments.

    Returns:
        str: The path to the configuration file.
    """
    if len(sys.argv) < 3:
        print(
            'Usage: python crawl_classic.py <site to crawl> ',
            '<function to check for med-content')
        sys.exit(1)

    sitename = sys.argv[1]
    if sitename.endswith('/'):
        sitename = sitename[:-1]

    function_str = sys.argv[2]
    function = getattr(_checker_funcs, function_str)

    return sitename, function


SITENAME, FUNCTION = handle_cmd_line_args()

NewCrawler = new_crawlers.CheckerCrawler(
    SITENAME,
    FUNCTION
)

NewCrawler.start_crawling()
