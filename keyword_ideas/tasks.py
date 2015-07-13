from __future__ import absolute_import

from celery import task, shared_task
from .models import SeedKeyword, Keyword
from .functions import get_adwords_client, get_keyword_ideas, get_google_top_10
from .mozapi import get_metrics

from time import sleep
import numpy as np

@task
def get_keyword_seo_metrics(keyword_list):
    count = 0 
    keywords = Keyword.objects.filter(phrase__in=keyword_list)
    print keywords
    for keyword in keywords:
        print 'Getting Google top 10 for %s' % keyword.phrase
        urls = get_google_top_10(keyword.phrase)
        print 'Getting SEO metrics from Moz for %s' % keyword.phrase
        metrics = get_metrics(urls)  

        print metrics
        # Extract metric into lists
        page_authorities = [m['upa'] for m in metrics]
        domain_authorities = [m['pda'] for m in metrics]
        external_page_links = [m['ueid'] for m in metrics]
        # Create numpy arrays from lists
        page_authorities_np = np.array(page_authorities)
        domain_authorities_np = np.array(domain_authorities)
        external_page_links_np = np.array(external_page_links)
        # Calculate mean and median
        mean_page_authority = int(round(np.mean(page_authorities_np),0))
        median_page_authority = int(round(np.median(page_authorities_np),0))
        mean_domain_authority = int(round(np.mean(domain_authorities_np),0))
        median_domain_authority = int(round(np.median(domain_authorities_np),0))
        mean_external_links = np.mean(external_page_links_np)
        median_external_links = np.mean(external_page_links_np)
        # Update keyword record
        keyword.mean_page_authority = mean_page_authority
        keyword.median_page_authority = median_page_authority
        keyword.mean_domain_authority = mean_domain_authority
        keyword.median_domain_authority = median_domain_authority
        keyword.mean_external_links = mean_external_links
        keyword.median_external_links = median_external_links
        print 'Saving keyword %s' % keyword.phrase
        keyword.save()

        count += 1
        if count < len(keywords):
            sleep(25)


    
@task
def get_seed_keyword_ideas(seed_keywords_list):
    client = get_adwords_client()
    seed_keywords = SeedKeyword.objects.filter(phrase__in=seed_keywords_list)
    print 'got client'
    for seed_keyword in seed_keywords:
        data = get_keyword_ideas(seed_keyword.phrase, client)
        for row in data[1:]:
            print row
            keyword = Keyword(
                    seed_keyword = seed_keyword,
                    phrase = row[0],
                    search_volume = int(row[1]),
                    average_cpc = row[2],
                    competition = row[3],
                    )
            keyword.save()
        print data




