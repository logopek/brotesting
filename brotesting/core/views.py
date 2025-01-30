from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from core.forms import QuizSolveForm
from .models import Course, Question, Quiz, Choice

from django.http import HttpResponse


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


class QuizCreateView(CreateView):
    model = Quiz
    template_name = 'core/quiz_create.html'
    fields = ['title','course', 'description', 'time_limit', 'passing_score']
    success_url = reverse_lazy('core:quiz_list')

    def form_valid(self, form):
        print("VALUE!!!")
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class QuizSolveView(DetailView):
    model = Quiz
    template_name = "core/quiz_solve.html"
    success_url = reverse_lazy('core:results')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=self.object)
        return context


class QuizAddQuestionsView(DetailView):
    model = Quiz
    template_name = 'core/quiz_addquestions.html'
    context_object_name = 'quiz'
    fields = '__all__'

class QuizEditView(UpdateView):
    model = Quiz
    template_name = "core/quiz_edit.html"
    fields = "__all__"

def take_quiz_view(request, pk):
    quiz = Quiz.objects.prefetch_related('questions').get(id=pk)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizSolveForm(questions, request.POST)
        if form.is_valid():
            return HttpResponse("<h1>Вы ответили</h1>" + str(form))
            pass
    else:
        form = QuizSolveForm(questions)

    return render(request, 'core/results.html', {'form': form, 'quiz': quiz})
