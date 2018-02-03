from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'polls'
urlpatterns = [
    url(r'^$',
        login_required(views.VoteView.as_view(), login_url='/polls/login'),
        name='vote'),
    url(r'^results/$',
        login_required(views.ResultsView.as_view(), login_url='/polls/login'),
        name='results'),
    url(r'^login/$',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(next_page='/polls/login'),
        name='logout')
]
