from tld import get_fld
from os import path
import urllib3

class WordMatcher(object):
    # use class vars for lazy loading
    MASTERURL = "http://www.greenteapress.com/thinkpython/code/words.txt"
    MASTERFILE = 'data/words.txt'
    WORDS = None

    @classmethod
    def fetch_words(cls, url=None):
        url = url or cls.MASTERURL

        # grab master list
        print ('fetching WORD list from server ...')
        lines = urllib3.urlopen(url).readlines()

        f = open(cls.MASTERFILE, 'w')
        f.writelines(lines)
        f.close()

    @classmethod
    def load_words(cls):
        f = open(cls.MASTERFILE, 'r')
        lines = f.readlines()
        f.close()

        # strip whitespaces
        # only words with more than three letters are considered
        lines = [ln for ln in (ln.strip() for ln in lines) if len(ln) > 3]
        cls.WORDS = {}
        for item in lines:
            cls.WORDS[item] = None
        #cls.WORDS = set(lines)

    def __init__(self):

        if path.exists(WordMatcher.MASTERFILE):
            WordMatcher.load_words()

        if WordMatcher.WORDS is None:
            WordMatcher.fetch_words()
            WordMatcher.load_words()

    def get_num_of_words(self, domain):
        num = 0
        for word in WordMatcher.WORDS:
            if word in domain:
                num += 1
        return num


def load_alexa(limit=None):
    """
    Reads top @limit number of popular domains based on alexa.com

    """
    alexa_domains = set()
    path = "data/top-1m.csv"
    with open(path) as f:
        for line in f:
            line = line.strip()
            sline = line.split(',')

            if limit and int(sline[0]) > limit:
                break

            """
            sometimes the Alexa list contains full URLs, e.g.
            example.com/path; need to get rid of that for later matching
            """
            domain = (sline[1].split('/'))[0]

            """
            we want only the 2LD+TLD, else we do not know later against what we
            need to match
            """
            sld_domain = get_fld(domain,fix_protocol=True)
            alexa_domains.add(sld_domain)
            alexa_domains.add(domain)
    alexa_slds = set([get_fld(el,fix_protocol=True) for el in alexa_domains])

    return alexa_slds

def load_words(path_to_data="data/top-1m.csv"):
    f = open(path_to_data, 'r')
    lines = f.readlines()
    f.close()

    # strip whitespaces
    # only words with more than three letters are considered
    lines = [ln for ln in (ln.strip() for ln in lines) if len(ln) > 3]
    words = set(lines)

    return words