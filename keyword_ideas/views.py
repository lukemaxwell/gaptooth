from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import SeedKeyword

def index(request):
    seed_keywords = SeedKeyword.objects.all()
    template = loader.get_template('keyword_ideas/index.html')
    context = RequestContext(request, {
        'seed_keywords': seed_keywords,
    })
    return HttpResponse(template.render(context))

def results(request, seed_keyword_id):
    response = "You're looking at the results for seed_keyword %s."
    return HttpResponse(response % seed_keyword_id)
