from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
]
