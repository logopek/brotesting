from django import forms
from .models import Quiz, Course, Question, StudentAnswer, Choice


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['title', 'course', 'description',
                  'time_limit', 'passing_score', 'created_by']

    def form_valid(self, form):
        print("VALUE!!!")
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class QuizSolveForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        """
        Инициализация формы. Для каждого вопроса добавляется соответствующее поле.
        """
        super().__init__(*args, **kwargs)

        for question in questions:
            field_name = f'question_{question.id}'
            if question.question_type == 'MCQ':  # Вопрос с выбором ответа
                self.fields[field_name] = forms.ModelChoiceField(
                    queryset=Choice.objects.filter(question=question),
                    widget=forms.RadioSelect,
                    label=question.question_text,
                    required=True
                )
            elif question.question_type == 'TF':  # True/False
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('True', 'Правда'), ('False', 'Ложь')],
                    widget=forms.RadioSelect,
                    label=question.question_text,
                    required=True
                )
            elif question.question_type == 'SA':  # Короткий текстовый ответ
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={"rows": 3}),
                    label=question.question_text,
                    required=False
                )