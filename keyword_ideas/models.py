from django.db import models

class SeedKeyword(models.Model):
    phrase = models.CharField(max_length=100, unique=True) 
    def __unicode__(self):
        return self.phrase
 
class Keyword(models.Model):
    seed_keyword = models.ForeignKey(SeedKeyword)
    phrase = models.CharField(max_length=100)
    search_volume = models.IntegerField()
    average_cpc = models.DecimalField(max_digits=5, decimal_places=2)
    competition = models.FloatField()
    mean_page_authority = models.IntegerField(null=True, blank=True)
    mean_domain_authority = models.IntegerField(null=True, blank=True)
    mean_external_links = models.FloatField(null=True, blank=True)
    median_page_authority = models.IntegerField(null=True, blank=True)
    median_domain_authority = models.IntegerField(null=True, blank=True)
    median_external_links = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.phrase

    class Meta:
          unique_together = ('seed_keyword', 'phrase',)
