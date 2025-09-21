# hifztracker/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),

    path('', home_view, name='home'),

    path('tracker/', include('apps.tracker.urls')),
]

# خدمة ملفات الميديا محليًا أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
