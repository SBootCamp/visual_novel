from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import offer_service.urls
import chart.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="pages/index.html"), name='main'),
    path('offers/', include(offer_service.urls), name='offers'),
    path('chart/', include(chart.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
