from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('admin/doc/',include('django.contrib.admindocs.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('telegram_bot.urls',
                     namespace='telegram_bot')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
