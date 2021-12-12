from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('', include('apps.sales.urls', namespace='sales')),
    path('quest/', include('apps.content.urls', namespace='content')),
    path('', include('social_django.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = 'apps.sales.views.page_not_found'
handler403 = 'apps.sales.views.page_not_found'
handler404 = 'apps.sales.views.page_not_found'
handler500 = 'apps.sales.views.page_not_found_500'
