
import re
from bs4 import BeautifulSoup


AI_PATTERN = r"(?i)\b((künstlich|artifiziell|artificial|super)\w*( (generell\w*|general))?\s?intelligen\w*|(intelligent|autonom)\w* (system|mas?chine)\w*|(mas?chin|supervise|überwacht|reinforce|bestärk|verstärk|gegnerisch|adversarial|deep|tief)\w*\s?(lernen|learning)|(neur\w* (netz|network)\w*)|(chat)?-?gpt|openai|gemini|copilot|bard|claude\s?\d|llama|(natural language processing|natürliche sprach-?verarbeitung|computer vision|bildverarbeitung|robot|deep\s?fake|large language model|sprachassisten|chatbot)\w*|\b(K|A)G?I\b|ML|NLP|LLM\b)"


TOPICS = (
    '/thema/ernaehrung/', '/thema/antropozaen/',
    '/thema/crispr-', 'thema/der-digitale-mensch',
    '/thema/gene-editing', '/thema/gruene-gentechnik',
    '/thema/informationstechnologie', '/thema/landwirtschaft',
    '/thema/kuenstliche-intelligenz', '/thema/landwirtschaft',
    '/thema/nachhaltigkeit', '/thema/roboter/', 'thema/unsere-ernaehrung',
    '/thema/verantwortungsvoll-fleisch', '/thema/waldleben'
)


def spektrum_is_ai(html, url):
    soup = BeautifulSoup(html, 'lxml')

    for topic in TOPICS:
        if topic in url:
            return True
    if not re.search(r'[0-9]{3}$', url):
        return True

    kywds = soup.find('meta', {'name': 'keywords'})
    if kywds is not None:
        kywds = kywds['content'].split(', ')
        for kywd in kywds:
            if re.search(AI_PATTERN, kywd):
                return True

    text = soup.get_text(separator=' ')
    if len(re.findall(AI_PATTERN, text)) > 2:
        return True

    return False


def infoakt_is_ai(html, url):
    if url:
        pass

    soup = BeautifulSoup(html, 'lxml')

    kywds = soup.find('meta', {'name': 'keywords'})

    link = soup.find('link', {'rel': 'canonical'})
    if not re.search(r'\.html$', link['href']):
        return True

    if kywds:
        for keyword in kywds['content'].split(', '):
            if re.search(AI_PATTERN, keyword):
                return True

    text = soup.get_text(separator=' ')
    if len(re.findall(AI_PATTERN, text)) > 1:
        return True

    return False


def array_element_in_string(array, string):
    for element in array:
        if element in string:
            return True
    return False


def zeit_is_health(html, _url):
    soup = BeautifulSoup(html, 'lxml')
    meta = soup.find_all('meta')
    if meta:
        for tag in meta:
            content = tag.get('content', '').lower()
            keywords = (
                'gesundheit', 'medizin', 'psychologie', 'krankenhaus',
                'ernaehrung', 'pflege'
            )
            if array_element_in_string(keywords, content):
                return True
    return False
