from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from core.forms import QuizSolveForm, QuestionForm, ChoiceFormSet
from .models import Course, Question, Quiz, Choice
from django.forms import inlineformset_factory
from core.parser import ResultParser
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Quiz, Question
from .forms import QuestionForm

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




class QuizAddQuestionsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if quiz.created_by != request.user:
            return HttpResponseForbidden()
        question_form = QuestionForm(initial={"quiz": pk})
        formset = ChoiceFormSet()
        return render(request, 'core/quiz_addquestions.html',
                      {'quiz': quiz, 'question_form': question_form, 'formset': formset})

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if quiz.created_by != request.user:
            return HttpResponseForbidden()

        question_form = QuestionForm(request.POST)

        if question_form.is_valid():

            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():

                formset.save()
                return redirect('core:quiz_detail', pk=quiz.pk)
        formset = ChoiceFormSet(request.POST)
        return render(request, 'core/quiz_addquestions.html',
                      {'quiz': quiz, 'question_form': question_form, 'formset': formset})


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
            resultParser = ResultParser()
            t = resultParser.parse(str(form), request.user)
            d = ""
            for i in t:
                if i.selected_choice is not None:
                    if i.selected_choice.is_correct:
                        d += f"<div><h2>{i.question.id}</h2> <p style='background: #B3FFCC'>t</p></div>"
                    else:
                        d += f"<div><h2>{i.question.id}</h2> <p style='background: #DB5C69'>f</p></div>"
                if i.tf_answer is not None:
                        d += f"<div><h2>{i.question.id}</h2> "

            return HttpResponse("<h1>Вы ответили</h1>" + str(d))

    else:
        form = QuizSolveForm(questions)

    return render(request, 'core/results.html', {'form': form, 'quiz': quiz})


class QuizViewOtherResults(LoginRequiredMixin, View):
    def get(self, request, pk):
        return HttpResponse("Hi!")
