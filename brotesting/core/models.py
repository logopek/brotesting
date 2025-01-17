from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """Учебная дисциплина"""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Преподаватель')
    students = models.ManyToManyField(
        User, related_name='enrolled_courses', verbose_name='Студенты')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')


class Quiz(models.Model):
    """Тест по предмету"""
    title = models.CharField('Название', max_length=200)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Дисциплина')
    description = models.TextField('Описание')
    time_limit = models.IntegerField('Ограничение по времени')
    passing_score = models.IntegerField('Проходной балл')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')


class Question(models.Model):
    """Вопрос в тесте"""
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    )

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, verbose_name='Тест')
    question_text = models.TextField(verbose_name='Текст вопроса')
    question_type = models.CharField(
        max_length=3, choices=QUESTION_TYPES, verbose_name='Тип вопроса')
    points = models.IntegerField(default=1, verbose_name='Баллы')


class Choice(models.Model):
    """Варианты ответа к вопросам"""
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    choice_text = models.CharField(max_length=200, verbose_name='Текст ответа')
    is_correct = models.BooleanField(
        default=False, verbose_name='Правильный ответ')


class QuizAttempt(models.Model):
    """Попытка прохождения теста"""
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Студент')
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, verbose_name='Тест')
    score = models.FloatField(null=True, blank=True, verbose_name='Баллы')
    started_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата начала')
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата завершения')


class StudentAnswer(models.Model):
    """Ответ ученика"""
    attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, verbose_name='Попытка')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Выбранный ответ')
    # Для тестов с открытым ответом
    text_answer = models.TextField(
        null=True, blank=True, verbose_name='Текстовый ответ')
    is_correct = models.BooleanField(
        null=True, verbose_name='Правильный ответ')


class QuizSettings(models.Model):
    """Настройки теста"""
    quiz = models.OneToOneField(
        Quiz, on_delete=models.CASCADE, verbose_name='Тест')
    shuffle_questions = models.BooleanField(
        default=False, verbose_name='Перемешать вопросы')
    show_results_immediately = models.BooleanField(
        default=True, verbose_name='Показывать результаты сразу')
    allow_review = models.BooleanField(
        default=True, verbose_name='Разрешить пересмотр')
    max_attempts = models.IntegerField(
        default=1, verbose_name='Максимальное количество попыток')


class StudentGroup(models.Model):
    """Учебный класс"""
    name = models.CharField('Название', max_length=100)
    students = models.ManyToManyField(
        User, verbose_name='Студенты')
    graduation_year = models.IntegerField('Год выпуска')
    courses = models.ManyToManyField(
        Course, related_name='groups', verbose_name='Дисциплины')

    def __str__(self):
        return f"{self.name} ({self.graduation_year})"
