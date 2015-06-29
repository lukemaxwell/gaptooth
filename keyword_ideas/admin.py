from django.contrib import admin
from .tasks import get_seed_keyword_ideas, get_keyword_seo_metrics
from .models import SeedKeyword, Keyword
from django.contrib import messages

def admin_get_seed_keyword_ideas(modelAdmin, request, queryset):
    seed_keyword_list = [s.phrase for s in queryset]
    get_seed_keyword_ideas.delay(seed_keyword_list)
    #get_seed_keyword_ideas.delay(seed_keywords=queryset)
    messages.success(request, 'Getting keyword ideas from Adwords for ' + ','.join([s.phrase for s in queryset]))

admin_get_seed_keyword_ideas.short_description=("Get seed keywords")

def admin_get_keyword_seo_metrics(modelAdmin, request, queryset):
    keyword_list = [s.phrase for s in queryset]
    get_keyword_seo_metrics.delay(keyword_list)
    #get_seed_keyword_ideas.delay(seed_keywords=queryset)
    messages.success(request, 'Getting seo metrics for %s ' % len(keyword_list))

admin_get_keyword_seo_metrics.short_description=("Get seo metrics")

class SeedKeywordAdmin(admin.ModelAdmin):
        fields = ['phrase']
        list_filter = ['phrase']
        ordering = ['phrase']
        actions = [admin_get_seed_keyword_ideas]

class KeywordAdmin(admin.ModelAdmin):
    fields = ['seed_keyword', 'phrase', 'search_volume', 'competition', 'average_cpc', 'mean_page_authority', 'mean_external_links']
    list_display = ['phrase', 'search_volume', 'competition', 'average_cpc', 'mean_page_authority', 'mean_domain_authority', 'mean_external_links']
    list_filter = ['seed_keyword__phrase']
    ordering = ['-search_volume', '-competition', '-average_cpc', 'phrase']
    actions = [admin_get_keyword_seo_metrics]

admin.site.register(SeedKeyword, SeedKeywordAdmin)
admin.site.register(Keyword, KeywordAdmin)
# Register your models here.
