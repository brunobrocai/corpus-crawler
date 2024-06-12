"""
This module contains the classes used to represent the objects
used in the crawling process and that differ between websites.

Author: Bruno Brocai
"""


import configparser
from dataclasses import dataclass
import os


@dataclass
class UrlPatterns:
    """Represents the patterns used to classify the URLs of the crawled site.

    Attributes:
        file_path (str): The path to the configuration file.
        patterns (dict): A dictionary containing the patterns for each section.
        article_pattern (str): Pattern used to classify article pages.
        notarticle_pattern (str): Pattern used to classify non-article pages.
        irrelevant_pattern (str): Pattern used to classify irrelevant pages.
        base_url (str): Base URL for the section.
    """

    file_path: str
    patterns: dict
    article_pattern: str
    notarticle_pattern: str
    irrelevant_pattern: str
    base_url: str

    def __init__(self, config, section):
        self.config = config
        self.patterns = self.load_patterns_from_config()
        self.article_pattern = self.patterns[section][1]
        self.notarticle_pattern = self.patterns[section][2]
        self.irrelevant_pattern = self.patterns[section][3]
        self.base_url = self.patterns[section][0]

    def load_patterns_from_config(self):
        patterns_dict = {}
        config = configparser.ConfigParser()
        config.read(self.config)

        for section in config.sections():
            patterns = [
                option for option in config.options(section)
                if 'url' in option
            ]
            section_patterns = [
                config.get(section, pattern) for pattern in patterns
            ]
            patterns_dict[section] = section_patterns

        return patterns_dict


@dataclass
class TrackingFiles:
    """Represents the files used to track the crawling process.

    Attributes:
        article (str): The directory where the article pages are stored.
        error (str): The directory where the urls causing errors are stored.
        queue (str): The directory where the urls in the queue are stored.
        visited (str): The directory where the visited urls are stored.
        graph (str): The directory where the graph is stored.
        irrelevant (str): The directory where the irrelevant urls are stored.
        forbidden (str): The directory where the forbidden urls are stored.
    """

    directory: str

    def __post_init__(self):
        self.error = f'{self.directory}/resources/error.txt'
        self.queue = f'{self.directory}/resources/queue.txt'
        self.visited = f'{self.directory}/resources/visited.txt'
        self.graph = f'{self.directory}/resources/graph.txt'
        self.irrelevant = f'{self.directory}/resources/irrelevant.txt'
        self.forbidden = f'{self.directory}/resources/forbidden.txt'

    @property
    def all_files_dict(self):
        return {
            'error_txt': self.error,
            'queue_txt': self.queue,
            'crawled_txt': self.visited,
            'graph_txt': self.graph,
            'irrelevant_txt': self.irrelevant,
            'forbidden': self.forbidden
        }


@dataclass
class GoalDirectory:
    """Represents the directory where the crawled data is stored.

    Attributes:
        directory (str): The directory where the data is stored.
        not_article (str): The directory where the non-article pages
            are stored.
        article (str): The directory where the article pages are stored.
    """

    directory: str

    def __post_init__(self):
        self.not_article = f'{self.directory}/nonarticle_pages'
        self.article = f'{self.directory}/article_pages'


@dataclass
class OldGoalDir:
    """Represents the directory where the crawled data is stored."""
    directory: str

    def __post_init__(self):
        self.not_article = f'{self.directory}/board_pages'
        self.article = f'{self.directory}/page_contents'


@dataclass
class MediaGoalDirectory(GoalDirectory):
    """Represents the directory where the media files are stored.

    Attributes:
        directory (str): The directory where the data is stored.
        not_article (str): The directory where the non-article pages
            are stored.
        article (str): The directory where the article pages are stored.
        images (str): The directory where the images are stored.
        pdf (str): The directory where the pdf files are stored.
        video (str): The directory where the video files are stored.
        audio (str): The directory where the audio files are stored.
    """

    def __post_init__(self):

        self.images = f'{self.directory}/images'
        self.imagecount = self.count_files(self.images)

        self.pdfs = f'{self.directory}/pdfs'
        self.pdfcount = self.count_files(self.pdfs)

        self.videos = f'{self.directory}/videos'
        self.videocount = self.count_files(self.videos)

        self.audios = f'{self.directory}/audios'
        self.audiocount = self.count_files(self.audios)

    def count_files(self, directory):
        # Initialize a counter for the number of files
        num_files = 0

        # Iterate over the files in the directory
        for _, _, files in os.walk(directory):
            # Increment the counter for each file
            num_files += len(files)

        return num_files


@dataclass
class MediaTrackingFiles(TrackingFiles):
    """Represents the files used to track the crawling process
    of media files.
    """

    indexdirs: MediaGoalDirectory

    def __post_init__(self):
        super().__post_init__()
        self.image_index = f'{self.indexdirs.images}/_index_.csv'
        self.pdf_index = f'{self.indexdirs.pdfs}/_index_.csv'
        self.video_index = f'{self.indexdirs.videos}/_index_.csv'
        self.audio_index = f'{self.indexdirs.audios}/_index_.csv'
