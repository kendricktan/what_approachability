from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analyze/?$', views.analyze, name='analyze'),
    url(r'^custom_url/?$', views.custom_url, name='custom_url'),
    url(r'^dump_json/(?P<url>.*)?/$', views.dump_json, name='dump_json'),
]
