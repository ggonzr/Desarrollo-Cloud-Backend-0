from django.urls import path
from django.conf.urls import include, url
from evento.views import event_list, event_detail

urlpatterns = [
    url('^$', event_list),
    url('^(?P<pk>.+)$', event_detail)
]