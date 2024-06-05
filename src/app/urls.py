from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('tz_detect/', include('tz_detect.urls')),
    path('', include('core.urls')),
]
