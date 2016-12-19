from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^upvote/$', views.upvote, name='upvote'),
    url(r'^survey/', views.survey, name='survey'),
    url(r'^prepare/', views.prepare, name='prepare'),
    url(r'^existing_survey/', views.existing_survey, name='existing_survey'),
    url(r'^get_surveys/', views.get_surveys, name='get_surveys'),
    #url(r'^get_surveys/(?P<user_id>[-\w]+)/', views.get_surveys, name='get_surveys'),
    url(r'^get_statistics/', views.get_statistics, name='get_statistics'),
    url(r'^reactivate/', views.reactivate, name='reactivate'),
    #url(r'^get_selected_survey/', views.get_selected_survey, name='get_selected_survey'),
    url(r'^login/$', auth_views.login, {'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/freequestion/login'}),

]
