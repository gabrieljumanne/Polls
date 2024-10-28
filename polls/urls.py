from django.urls import path

from . import views

#namespace for my app . 
app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="main"),
    path("<int:pk>/", views.DetailView.as_view(), name='detail'),
    path("<int:pk>/results/", views.ResultView.as_view(), name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote"), #manage the vote action 
    
]
