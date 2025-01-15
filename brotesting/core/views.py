from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth import logout

from .models import Course, Question, Quiz


class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html')


class QuizListView(ListView):
    model = Quiz
    template_name = 'core/quiz_list.html'
    context_object_name = 'quizzes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'core/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=self.object)
        return context
