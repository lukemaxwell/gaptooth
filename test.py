from keyword_ideas.tasks import get_seed_keyword_ideas, get_keyword_seo_metrics 
from keyword_ideas.models import SeedKeyword, Keyword

#seed_keywords = SeedKeyword.objects.all()
#get_seed_keyword_ideas(seed_keywords)
keywords = Keyword.objects.filter(text='electric bike battery')
get_keyword_seo_metrics(keywords)

