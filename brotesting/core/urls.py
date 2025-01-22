from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/solve', views.QuizSolveView.as_view(), name='quiz_solve'),
    path('quizzes/<int:pk>/edit', views.QuizEditView.as_view(), name='quiz_edit'),
    path('quizzes/<int:pk>/addquestions', views.QuizAddQuestionsView.as_view(), name="quiz_addquestions"),
    path('quizzes/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quizzes/<int:pk>/results', views.results, name='results')
]
