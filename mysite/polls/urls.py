from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static

from mysite import settings
from . import views

app_name = 'polls'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('registration/', views.regView, name='reg'),
    path('registration/login', views.MyLoginView.as_view(), name='login'),
    path('accounts/<int:pk>', views.Profile.as_view(), name='profile'),
    path('delete_profile/<int:pk>', views.delete_profile, name='del_prof'),
    path('polls/logout/', LogoutView.as_view(), name='logout'),
    path('historylist/', views.HistoryList.as_view(), name='history'),
]

