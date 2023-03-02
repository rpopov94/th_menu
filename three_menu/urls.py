from django.urls import path, re_path
from django.contrib import admin

from menu.views import my_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_view),
    re_path(r'^(.*)/$', my_view, name='index')
]
