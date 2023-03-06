from django.urls import path, re_path, include
from django.contrib import admin

from menu.views import my_view

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_view),
    re_path(r'^(.*)/$', my_view, name='index')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns