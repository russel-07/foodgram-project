from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500 
from django.contrib.flatpages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('app_users.urls')),
    path('api/', include('app_api.urls')),
    path('', include('app_recipes.urls')),
]

urlpatterns += [
    path('about-author/', views.flatpage, {'url': '/about/author/'}, name='about'),
]


handler404 = "app_recipes.misc.page_not_found"  # noqa
handler500 = "app_recipes.misc.server_error"  # noqa


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
