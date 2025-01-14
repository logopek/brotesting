from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """Учебная дисциплина"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses')
    created_at = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    """Тест по предмету"""
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    passing_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    """Вопрос в тесте"""
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    points = models.IntegerField(default=1)


class Choice(models.Model):
    """Варианты ответа к вопросам"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class QuizAttempt(models.Model):
    """Попытка прохождения теста"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class StudentAnswer(models.Model):
    """Ответ ученика"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True)
    # Для тестов с открытым ответом
    text_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True)


class QuizSettings(models.Model):
    """Настройки теста"""
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    shuffle_questions = models.BooleanField(default=False)
    show_results_immediately = models.BooleanField(default=True)
    allow_review = models.BooleanField(default=True)
    max_attempts = models.IntegerField(default=1)
