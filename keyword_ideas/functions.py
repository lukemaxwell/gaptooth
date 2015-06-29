#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example retrieves keywords that are related to a given keyword.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

Tags: TargetingIdeaService.get
Api: AdWordsOnly
"""

from googleads import adwords
from operator import itemgetter
from .googlespider import GoogleSpider
# Globals
PAGE_SIZE = 100

def get_google_top_10(keyphrase):
    spider = GoogleSpider(keyphrase, max_results=10)
    results = spider.crawl()
    urls = [r[0] for r in results]
    return urls 



def get_adwords_client():
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    return adwords_client


def get_keyword_ideas(keyphrase, client):
    print 'Initializing adwords targetting idea service'
    targeting_idea_service = client.GetService(
            'TargetingIdeaService', version='v201502')
    # Construct selector object and retrieve related keywords.
    offset = 0
    selector = {
            'searchParameters': [
                    {
                            'xsi_type': 'RelatedToQuerySearchParameter',
                            'queries': [keyphrase]
                    },
                    {
                            # Language setting (optional).
                            # The ID can be found in the documentation:
                            #  https://developers.google.com/adwords/api/docs/appendix/languagecodes
                            'xsi_type': 'LanguageSearchParameter',
                            'languages': [{'id': '1000'}]
                    },
                    #{
                    #        # Language setting (optional).
                    #        # The ID can be found in the documentation:
                    #        #  https://developers.google.com/adwords/api/docs/appendix/languagecodes
                    #        'xsi_type': 'LocationSearchParameter',
                    #        'locations': [{'id': '2826'}]
                    #}
            ],
            'ideaType': 'KEYWORD',
            'requestType': 'IDEAS',
            'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME', 'AVERAGE_CPC', 'COMPETITION',
                                                                    'CATEGORY_PRODUCTS_AND_SERVICES'],
            'paging': {
                    'startIndex': str(offset),
                    'numberResults': str(PAGE_SIZE)
            }
    }
    more_pages = True
    data = [['keyword', 'search_volume', 'average_cpc', 'competition', 'competition_class']]
    while more_pages:
        print 'Running query'
        page = targeting_idea_service.get(selector)

        # Display results.
        if 'entries' in page:
            for result in page['entries']:
                attributes = {}
                for attribute in result['data']:
                    attributes[attribute['key']] = getattr(attribute['value'], 'value',
                                                                                                  '0')
                #print ('%s, %s, %s, %s' % (attributes['KEYWORD_TEXT'], attributes['SEARCH_VOLUME'], attributes['AVERAGE_CPC'], attributes['COMPETITION']))
                try:
                        average_cpc = round(attributes['AVERAGE_CPC'].microAmount/float(100000),2)
                except:
                        average_cpc = 0
                competition = round(attributes['COMPETITION'],2)
                if competition > 0.7:
                    competition_class = 'HIGH'
                elif competition > 0.4:
                    competition_class = 'MEDIUM'
                else:
                    competition_class = 'LOW'
                row = [str(attributes['KEYWORD_TEXT']), attributes['SEARCH_VOLUME'], average_cpc, competition, competition_class]
                data.append(row)
            data = sorted(data, key=itemgetter(1), reverse=True)
        else:
            print 'No related keywords were found.'
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])
        return data

