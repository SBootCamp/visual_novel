from django.http import HttpResponse

from translation.models import TranslationStatistics


# Create your views here.
def index(request):
    stats_list = TranslationStatistics.objects.all()
    # output = ', '.join([q.question_text for q in stats_list])
    return HttpResponse(stats_list)
