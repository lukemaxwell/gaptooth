from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Sum

from .models import SeedKeyword, Keyword
from .functions import get_moz_score, get_links_score, get_search_volume_score, get_opportunity_score

def index(request):
    seed_keywords = SeedKeyword.objects.all()
    template = loader.get_template('keyword_ideas/index.html')
    context = RequestContext(request, {
        'seed_keywords': seed_keywords,
    })
    return HttpResponse(template.render(context))

def results(request, seed_keyword_id):
    keywords = Keyword.objects.filter(seed_keyword__id=seed_keyword_id)
    total_searches = keywords.aggregate(Sum('search_volume'))['search_volume__sum']
    total_external_links = keywords.aggregate(Sum('mean_external_links'))['mean_external_links__sum']
    keyword_ideas = []
    for keyword in keywords:
        search_volume_score = get_search_volume_score(keyword.search_volume, total_searches)
        domain_authority_score = get_moz_score(keyword.median_domain_authority)
        page_authority_score = get_moz_score(keyword.median_page_authority)
        links_score = get_links_score(keyword.median_external_links, total_external_links)

        opportunity_score = get_opportunity_score(
                search_volume_score,
                domain_authority_score,
                page_authority_score,
                links_score
                )

        k = {
            'phrase': keyword.phrase,
            'search_volume': keyword.search_volume,
            'mean_domain_authority': keyword.median_domain_authority,
            'mean_page_authority': keyword.median_page_authority,
            'mean_external_links': keyword.median_external_links,
            'opportunity_score': opportunity_score
        }
        keyword_ideas.append(k)
    template = loader.get_template('keyword_ideas/keywords.html')
    context = RequestContext(request, {
        'keyword_ideas': keyword_ideas,
    })
    return HttpResponse(template.render(context))
