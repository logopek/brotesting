from django import forms
from .models import Quiz, Course, Question, StudentAnswer


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['title', 'course', 'description',
                  'time_limit', 'passing_score']



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = '__all__'