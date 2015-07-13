import argparse
import urllib2
import sys
import tldextract
import requests
import logging
from urllib import quote_plus
from bs4 import BeautifulSoup
from lxml import html as ht
from time import sleep
from googleparser import Parser

from random import choice, uniform

class GoogleSpider():

    proxies = {}
    phrase = None
    proxy = None
    user_agents = None
    max_results = None
    wait_time = None 
    def __init__(self, phrase, country='gb', proxy=None, language=None, results_per_page=100, max_results=20):
        self.phrase = quote_plus(phrase)
        self.max_results = max_results 
        self.country = country.lower()
        self.language = language
        self.wait_time = 30
        self.results_per_page = results_per_page
        self.proxy = proxy
        self.search_urls = {
            'gb': 'https://www.google.co.uk/search?gl=gb&q=',
            'us': 'https://www.google.com/search?gl=us&q=',
            'ca': 'https://www.google.ca/search?gl=ca&q=',
            'cl': 'https://www.google.cl/search?gl=cl&q=',
            'co': 'https://www.google.com.co/search?gl=co&q=',
            'br': 'https://www.google.com.br/search?gl=br&q=',
            'ie': 'https://www.google.ie/search?gl=ie&q=',
            'qa': 'https://www.google.com.qa/search?gl=qa&q=',
            'mx': 'https://www.google.com.mx/search?gl=mx&q=',
            'pe': 'https://www.google.com.pe/search?gl=pe&q=',
            'ar': 'https://www.google.com.ar/search?gl=ar&q=',
            'au': 'https://www.google.com.au/search?gl=au&q=',  
            
        }
        self.languages = {
            'br': 'pt-br',
            'gb': 'en-gb',
            'us': 'en-us',
            'cl': 'es-cl',
            'co': 'es-co',
            'ie': 'en-ie',
            'mx': 'es-mx',
            'ar': 'es-ar',
            'pe': 'es-pe',
            'au': 'en-au',
        }
        if self.language is None:
            self.language = self.languages[country]

        self.search_url = self.search_urls[self.country]
            
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11;',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0;',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17;',
        ]
    
    def crawl(self):
        rank = 1
        start = 0
        wait = 15
        url = None
        results = []
        parser = Parser()
        
        while len(results) < self.max_results:
            #if url is None:
            #    referer = 'https://www.google.co.uk/webhp?hl=en&tab=ww'
            #else:
            #    referer = url
            if url is not None:
                referer = url
            else:
                referer = None
            url = '%s%s&start=%s&num=%s' % (self.search_url,self.phrase,start, self.results_per_page)
            #print url
            html = None          
            version = 'common'
            proxies = {
                'http': self.proxy,
                'https:': self.proxy
            }  
            ua = choice(self.user_agents),
            #print ua 

            headers = {
                #'User-Agent': choice(self.user_agents),
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': referer,
                'Accept-Language': self.language,
                'Accept-Encoding': 'gzip, deflate',
                #'Connection': 'close',
                #'DNT': '1'
            }   
            #print 'Requesting %s' % url
            print url
            response = requests.get(url, headers=headers, proxies=proxies, verify=False)
            if response.status_code == 503:
                print 'Failed to access %s' % url 
                sys.exit(2)
           
            html = response.text
            items = parser.parse(html) 
            results += items
            # Include a wait time, and increment start index if we are not finished collecting data
            if len(results) < self.max_results:
                start += self.results_per_page
                sleep(self.wait_time)
        results = results[:self.max_results] # trim to max result size
        return results 

def get_phrases_from_file(file_path):
    phrases = []
    try:
        f = open(file_path)
        phrases = [l for l in (line.strip() for line in f) if l]
        f.close()
    except:
        print 'Could not open phrase file'
        sys.exit(2)
    if len(phrases) == 0:
        print 'Phrase file empty'
        sys.exit(2)
    return phrases 

def main(argv):
    phrase = None
    input_file = None
    country = 'gb' 
    proxy = None
    max_results = 20 
    language = None
    results_per_page = 100

    argparser = argparse.ArgumentParser(add_help=True)

    argparser.add_argument('--phrase',
                     help=('The search phrase you would like input into Google.'
                          'Format is xxx where xxx is your phrase, or /xx/xx/xx/xx.csv|txt where /xx/xx/xx/ is the folder path, and xx.csv/txt is the name of the file'))

    argparser.add_argument('--country', type=str,
                     help=('The country you would like to use as a location for Google. This changes the the search URL to the appropriate Google domain, e.g. google.co.uk, google.com, google.fr.'
                          'Format is xx where xx is the two letter ISO country code.'))
                     
    argparser.add_argument('--file', 
                     help=('Path to file containing phrases on seperate lines as your phrase input, and the googlespider will search for each of the phrases in the file.'
                          'Format is /PATH/TO/FILE.txt|CSV'))

    argparser.add_argument('--proxy', 
                     help=('The proxy string you would like to use.'
                         'Format is USERNAME:PASSWORD@IP:PORT.'))

    argparser.add_argument('--language', type=str,
                     help=('The value of the ACCEPT-LANGUAGE request header. Can affect results returned by Google.'
                         'Format is [2-letter language code]-[2-letter country code], or [2 letter language code]. Examples are en-gb, en-us, es-cl, and en. More examples here: https://msdn.microsoft.com/en-gb/library/ee825488(v=cs.20).aspx'))
                     
    argparser.add_argument('--max', type=int,
                     help=('The max number of results you would like to check.'
                         'Format is xxx where xxx is an integer between 1 and 1000.'))

    argparser.add_argument('--results-per-page', type=int,
                     help=('The number of results per page.'
                         'Format is an integer between 1 and 100.'))
    

    args = argparser.parse_args()

    if args.proxy:
        proxy = args.proxy
    if args.phrase:
        phrase = args.phrase
    if args.country:
        country = args.country
    if args.file:
        input_file = args.file
    if args.language:
        language = args.language
    if args.results_per_page:
        results_per_page = args.results_per_page
    if args.max:
        max_results = args.max
        
    # Ensure user as supplied minimum requirements - either a phrase or a path to file, but not both
    if (input_file is None and phrase is None) or (input_file is not None and phrase is not None):
        print 'Supply either --file /PATH/TO/FILE.txt|CSV or --phrase PHRASE'
        sys.exit()

    if input_file is not None:
        phrases = get_phrases_from_file(input_file)
        count = 0
        for phrase in phrases:
            spider = GoogleSpider(phrase=phrase, country=country, language=language, results_per_page=results_per_page, max_results=max_results,proxy=proxy)
            results = spider.crawl()
            rank = 1
            for result in results:
                print '%s\t%s\t%s\t%s' % (phrase, rank, result[0], result[3])
                rank += 1
            count += 1
            if count < len(phrases):
                sleep(spider.wait_time)

    else:
        spider = GoogleSpider(phrase=phrase, country=country, language=language, results_per_page=results_per_page, max_results=max_results,proxy=proxy)
        results = spider.crawl()
        rank = 1
        for result in results:
            print '%s\t%s\t%s\t%s' % (args.phrase, rank, result[0], result[3])
            rank += 1

if __name__ == '__main__':
    main(sys.argv[1:])
