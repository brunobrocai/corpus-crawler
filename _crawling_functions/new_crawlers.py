import time
import datetime
import random
import re
from urllib import robotparser
import mimetypes
import requests
from . import crawling_objects
from . import check_relevance
from . import retrieve_data
from . import write_data
from . import special_funcs as special


def lists_dontcrawl_tocrawl_regex(
    crawllinks, dontlinks,
    startsw_regex, notinclude_list
):

    dont_crawl = retrieve_data.read_linklist(dontlinks)
    to_crawl = retrieve_data.read_linklist(crawllinks)
    print(f'Links to crawl in list: {len(to_crawl)}')
    to_crawl = check_relevance.relevant_set_regex(
                to_crawl,
                excludes_pattern=notinclude_list
            )
    print(f'Relevant links after irrelevant exclusion: {len(to_crawl)}')
    to_crawl = check_relevance.set_elements_startwith_regex(
                to_crawl,
                startsw_regex
            )
    print(f'Relevant links after startswith exclusion: {len(to_crawl)}')
    print(f'Links not to crawl in list: {len(dont_crawl)}')
    to_crawl = check_relevance.remove_subset(to_crawl, dont_crawl)

    return to_crawl, dont_crawl


def list_dontcrawl_tocrawl_index(
    mediatracking
):

    to_crawl = retrieve_data.read_linklist(mediatracking.queue)

    dont_crawl = retrieve_data.read_index_csv(
        mediatracking.image_index
    )
    dont_crawl = dont_crawl | retrieve_data.read_index_csv(
        mediatracking.pdf_index
    )
    dont_crawl = dont_crawl | retrieve_data.read_index_csv(
        mediatracking.video_index
    )
    dont_crawl = dont_crawl | retrieve_data.read_index_csv(
        mediatracking.audio_index
    )

    to_crawl = check_relevance.remove_subset(to_crawl, dont_crawl)

    return to_crawl, dont_crawl


class Crawler():
    """
    General class for web crawlers.
    """

    def __init__(self, website, config='patterns.ini'):

        # Get the objects needed
        self.url_patterns = crawling_objects.UrlPatterns(
            config, website
        )
        self.dir_structure = crawling_objects.GoalDirectory(
            website
        )
        self.tracking_files = crawling_objects.TrackingFiles(
            website
        )

        # Initiate the check for robots.txt
        self._rp = self.make_robots_checker()

        # Initiate the queue and visited sets
        self._to_crawl, self._crawled_urls = lists_dontcrawl_tocrawl_regex(
            self.tracking_files.queue,
            self.tracking_files.visited,
            (f'{self.url_patterns.article_pattern}'
             f'|{self.url_patterns.notarticle_pattern}'),
            self.url_patterns.irrelevant_pattern
        )

        # If there's nothing to crawl, check the base url for new content
        if len(self._to_crawl) < 1:
            self._to_crawl.add(self.url_patterns.base_url + '/')

    def make_robots_checker(self):
        """Create a robotparser object to check robots.txt."""
        rp = robotparser.RobotFileParser()
        rp.set_url(
            self.url_patterns.base_url + '/robots.txt')
        try:
            rp.read()
            print('Successfully read robots.txt')
        except Exception as e:
            print(f'Error reading robots.txt: {e}')
            rp = None
        return rp

    def ready_to_crawl(self):
        """Check if the crawler is ready to start crawling."""
        if len(self._to_crawl) == 0:
            raise ValueError('No links to crawl.')
        if len(self._crawled_urls) == 0:
            print('WARNING! No crawled URLs specified. Is this correct?')
        return True

    def continue_crawling(self, max_pages, page_count, to_crawl):
        """
        Determine whether the crawl should continue.

        Args:
            max_pages (int): The maximum number of pages to crawl.
            page_count (int): The current number of pages crawled.
            to_crawl (set): The set of URLs to crawl.

        Returns:
            bool: True if the crawl should continue, False otherwise.
        """
        return (
            (max_pages is None or page_count < int(max_pages))
            and to_crawl
        )

    def sort_incoming_links(self, new_links):

        new_links = special.make_absolute_links(
            new_links,
            self.url_patterns.base_url
        )
        relevant_links = check_relevance.relevant_set_regex(
            new_links,
            starts_pattern=(
                f'{self.url_patterns.article_pattern}|'
                f'{self.url_patterns.notarticle_pattern}'
            ),
            excludes_pattern=self.url_patterns.irrelevant_pattern
        )
        irrel_links = new_links - relevant_links
        relevant_links = check_relevance.remove_subset(
            relevant_links,
            self.crawled_urls
        )

        return relevant_links, irrel_links

    def wait_random_time(self, min_time=3, max_time=7):
        waittime = random.uniform(min_time, max_time)
        time.sleep(waittime)

    def start_crawling(self, max_pages=None):
        pass

    @property
    def to_crawl(self):
        return self._to_crawl

    @to_crawl.setter
    def to_crawl(self, links):
        self._to_crawl = links

    @property
    def crawled_urls(self):
        return self._crawled_urls

    @crawled_urls.setter
    def crawled_urls(self, links):
        self._crawled_urls = links


class ClassicCrawler(Crawler):
    """
    Crawl domains where the board and post urls are a regex pattern.
    """

    def start_crawling(self, max_pages=None):
        """
        Crawls a set of start links up to a maximum number of pages.

        This function performs a breadth-first search (BFS) starting from the
        provided start links. It keeps track of the URLs it has already crawled
        to avoid duplicates. If a URL is a post URL, it saves the HTML content.
        If a URL is a board URL, it saves the HTML content and adds the URL to
        the set of URLs to crawl.

        Args:
            start_links (set): The set of URLs to start crawling from.
            crawled_urls (set): The set of URLs that have already been crawled.
            max_pages (int): The maximum number of pages to crawl.
            poststr (str): String to identify post URLs.
            boardstr (str): String to identify board URLs.
            notinclude (str): String to identify URLs to exclude from crawling.
        """
        page_count = 0

        if not self.ready_to_crawl():
            return None

        # Main crawling loop
        while super().continue_crawling(max_pages, page_count, self.to_crawl):

            page_count += 1
            next_url = self._to_crawl.pop()
            write_data.append_line_to_file(
                self.tracking_files.visited,
                next_url
            )

            try:
                self.crawled_urls.add(next_url)
                print(f'{page_count}: ', next_url)
                html = retrieve_data.get_html_from_url(next_url)

                # If the URL is a post URL, save the HTML content
                if re.match(self.url_patterns.article_pattern, next_url):
                    write_data.write_html_to_json(
                            self.dir_structure.article,
                            next_url,
                            html
                        )

                # If the URL is a board URL, save the HTML content and add URL
                elif (
                    re.match(self.url_patterns.notarticle_pattern, next_url)
                ):
                    write_data.write_html_to_json(
                            self.dir_structure.not_article,
                            next_url,
                            html
                        )
                else:
                    write_data.append_line_to_file(
                        self.tracking_files.irrelevant,
                        next_url
                    )

                # Extract links from the HTML content
                # and add them to the set to crawl
                new_links = retrieve_data.get_links_from_html(
                    html
                )
                relevant_links, irrel_links = self.sort_incoming_links(
                    new_links
                )

                self.to_crawl = self.to_crawl | relevant_links

                write_data.append_lines_to_file(
                    self.tracking_files.queue,
                    relevant_links
                )
                write_data.append_lines_to_file(
                    self.tracking_files.irrelevant,
                    irrel_links
                )

                write_data.append_line_to_file(
                    self.tracking_files.graph,
                    str(len(self.to_crawl))
                )

                # Randomize wait time so it's a little less sus
                self.wait_random_time()

            except (
                ValueError,
                TypeError,
                FileExistsError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError
            ) as e:
                write_data.append_line_to_file(
                    self.tracking_files.error,
                    next_url
                )
                print(e)
                self.wait_random_time()

        write_data.append_line_to_file(
            self.tracking_files.graph,
            str(len(self.to_crawl))
        )

        return None


class CheckerCrawler(Crawler):
    """
    Crawl domains where the board and post urls are a regex pattern
    and a checker function is provided to determine if the page is relevant.
    """

    def __init__(
        self, website, checker_func, check_board=True, config='patterns.ini'
    ):
        self.checker_func = checker_func
        self.check_for_board = check_board
        super().__init__(website, config)

    def start_crawling(self, max_pages=None):
        """
        Crawls a set of start links up to a maximum number of pages.

        This function performs a breadth-first search (BFS) starting from the
        provided start links. It keeps track of the URLs it has already crawled
        to avoid duplicates. If a URL is a post URL, it saves the HTML content.
        If a URL is a board URL, it saves the HTML content and adds the URL to
        the set of URLs to crawl.

        Args:
            start_links (set): The set of URLs to start crawling from.
            crawled_urls (set): The set of URLs that have already been crawled.
            max_pages (int): The maximum number of pages to crawl.
            poststr (str): String to identify post URLs.
            boardstr (str): String to identify board URLs.
            notinclude (str): String to identify URLs to exclude from crawling.
        """
        page_count = 0

        if not self.ready_to_crawl():
            return None

        # Main crawling loop
        while super().continue_crawling(max_pages, page_count, self.to_crawl):

            page_count += 1
            next_url = self._to_crawl.pop()
            write_data.append_line_to_file(
                self.tracking_files.visited,
                next_url
            )

            try:
                self.crawled_urls.add(next_url)
                print(f'{page_count}: ', next_url)
                html = retrieve_data.get_html_from_url(next_url)

                check = self.checker_func(html, next_url)
                checkboard = check and self.check_for_board

                # If the URL is a post URL, save the HTML content
                if (
                    re.match(self.url_patterns.article_pattern, next_url)
                    and check
                ):
                    write_data.write_html_to_json(
                            self.dir_structure.article,
                            next_url,
                            html
                        )

                # If the URL is a board URL, save the HTML content and add URL
                elif (
                    re.match(self.url_patterns.notarticle_pattern, next_url)
                    and checkboard
                ):
                    write_data.write_html_to_json(
                            self.dir_structure.not_article,
                            next_url,
                            html
                        )
                else:
                    write_data.append_line_to_file(
                        self.tracking_files.irrelevant,
                        next_url
                    )
                    write_data.append_line_to_file(
                        self.tracking_files.graph,
                        str(len(self.to_crawl))
                    )
                    self.wait_random_time()
                    continue

                # Extract links from the HTML content
                # and add them to the set to crawl
                new_links = retrieve_data.get_links_from_html(
                    html
                )
                relevant_links, irrel_links = self.sort_incoming_links(
                    new_links
                )
                self.to_crawl = self.to_crawl | relevant_links

                write_data.append_lines_to_file(
                    self.tracking_files.queue,
                    relevant_links
                )
                write_data.append_lines_to_file(
                    self.tracking_files.irrelevant,
                    irrel_links
                )

                write_data.append_line_to_file(
                    self.tracking_files.graph,
                    str(len(self.to_crawl))
                )

                # Randomize wait time so it's a little less sus
                self.wait_random_time()

            except (
                ValueError,
                TypeError,
                FileExistsError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError
            ) as e:
                write_data.append_line_to_file(
                    self.tracking_files.error,
                    next_url
                )
                print(e)
                self.wait_random_time()

        write_data.append_line_to_file(
            self.tracking_files.graph,
            str(len(self.to_crawl))
        )

        return None


class ListedMediaCrawler(Crawler):
    """
    Crawl domains where the board and post urls are a regex pattern
    and a checker function is provided to determine if the page is relevant.
    """

    def __init__(self, website, delay=(2, 6)):
        try:
            super().__init__(website)
        except (ValueError, KeyError):
            pass

        self.dir_structure = crawling_objects.MediaGoalDirectory(
            website
        )
        self.tracking_files = crawling_objects.MediaTrackingFiles(
            website, self.dir_structure
        )
        self._to_crawl, self._crawled_urls = list_dontcrawl_tocrawl_index(
            self.tracking_files
        )
        self.delay = delay

    def filetype(self, url):
        filetype = mimetypes.guess_type(url)[0]
        if filetype:
            return filetype.split('/')[0], filetype.split('/')[1]
        return None

    def index_entry(self, url, number, extension):
        return (
            f'"{number}",'
            f'"{str(datetime.datetime.now())}",'
            f'"{url}.{extension}"'
        )

    def start_crawling(self, max_pages=None):

        page_count = 0

        if not self.ready_to_crawl():
            return None

        # Main crawling loop
        while super().continue_crawling(max_pages, page_count, self.to_crawl):

            page_count += 1
            next_url = self._to_crawl.pop()
            write_data.append_line_to_file(
                self.tracking_files.visited,
                next_url
            )

            try:
                self.crawled_urls.add(next_url)
                print(f'{page_count}: ', next_url)
                mimetype, extension = self.filetype(next_url)
                binary_content = retrieve_data.get_content_from_url(next_url)

                # If the URL is a post URL, save the HTML content
                if mimetype == 'image':
                    self.dir_structure.imagecount += 1
                    index_line = self.index_entry(
                        self.dir_structure.imagecount,
                        next_url,
                        extension
                    )
                    write_data.save_indexed_media(
                        binary_content,
                        self.dir_structure.images,
                        self.dir_structure.imagecount,
                        extension,
                    )
                    write_data.append_line_to_file(
                        self.tracking_files.image_index,
                        index_line
                    )

                # If the URL is a board URL, save the HTML content and add URL
                elif mimetype == 'application' and extension == 'pdf':
                    self.dir_structure.pdfcount += 1
                    index_line = self.index_entry(
                        self.dir_structure.pdfcount,
                        next_url,
                        extension
                    )
                    write_data.save_indexed_media(
                        binary_content,
                        self.dir_structure.pdfs,
                        self.dir_structure.pdfcount,
                        extension
                    )
                    write_data.append_line_to_file(
                        self.tracking_files.pdf_index,
                        index_line
                    )

                elif mimetype == 'video':
                    self.dir_structure.videocount += 1
                    index_line = self.index_entry(
                        self.dir_structure.videocount,
                        next_url,
                        extension
                    )
                    write_data.save_indexed_media(
                        binary_content,
                        self.dir_structure.videos,
                        self.dir_structure.videocount,
                        extension
                    )
                    write_data.append_line_to_file(
                        self.tracking_files.video_index,
                        index_line
                    )

                elif mimetype == 'audio':
                    self.dir_structure.audiocount += 1
                    index_line = self.index_entry(
                        self.dir_structure.audiocount,
                        next_url,
                        extension
                    )
                    write_data.save_indexed_media(
                        binary_content,
                        self.dir_structure.audios,
                        self.dir_structure.audiocount,
                        extension
                    )
                    write_data.append_line_to_file(
                        self.tracking_files.audio_index,
                        index_line
                    )

                write_data.append_line_to_file(
                    self.tracking_files.graph,
                    str(len(self.to_crawl))
                )

                # Randomize wait time so it's a little less sus
                self.wait_random_time(self.delay[0], self.delay[1])

            except (
                ValueError,
                TypeError,
                FileExistsError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError
            ) as e:
                write_data.append_line_to_file(
                    self.tracking_files.error,
                    next_url
                )
                print(e)
                self.wait_random_time()

        write_data.append_line_to_file(
            self.tracking_files.graph,
            str(len(self.to_crawl))
        )

        return None
