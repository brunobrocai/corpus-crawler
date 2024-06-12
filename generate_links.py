import sys
from _crawling_functions import special_funcs


def handle_cmd_line_args():
    """Handle the command line arguments.

    Returns:
        str: The path to the configuration file.
    """
    if len(sys.argv) < 4:
        print(
            'Usage: python generate_links.py <place_to_add_links> ',
            '<function to generate links> <number of pages>')
        sys.exit(1)

    sitename = sys.argv[1]
    if sitename.endswith('/'):
        sitename = sitename[:-1]

    function_str = sys.argv[2]
    function = getattr(special_funcs, function_str)

    amount = int(sys.argv[3])

    try:
        special_param1 = sys.argv[4]
    except IndexError:
        special_param1 = None

    return sitename, function, amount, special_param1


SITENAME, FUNCTION, AMOUNT, SPECIAL_PARAM = handle_cmd_line_args()

queue = f'{SITENAME}/resources/queue.txt'

if SPECIAL_PARAM:
    FUNCTION(AMOUNT, queue, SPECIAL_PARAM)
else:
    FUNCTION(AMOUNT, queue)

# NewCrawler = new_crawlers.ClassicCrawler(
#     SITENAME
# )

# NewCrawler.start_crawling()
