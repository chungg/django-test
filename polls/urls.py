from django.conf.urls import url

from . import views


app_name = 'polls'
urlpatterns = [
    url(r'^$', views.VoteView.as_view(), name='vote'),
    url(r'^results/$', views.ResultsView.as_view(),
        name='results'),
]
