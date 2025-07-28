from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from home.models import Post  # Post modeli bo‘lishi shart

info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'created_at',
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('booking/', include('booking.urls')),
    path('price/', include('price.urls')),
    path('navigate/', include('navigate.urls')),

    # SEO fayllar
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': {'posts': GenericSitemap(info_dict, priority=0.6)}}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
