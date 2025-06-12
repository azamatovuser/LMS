from django.db import models
from apps.course.models import Lesson, Module

class TimeStamp(models.Model):
    order = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class LocalizationItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    language_type = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Quiz(TimeStamp):
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)

class QuizLocalizationItem(LocalizationItem):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Question(TimeStamp):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class QuestionLocalizationItem(LocalizationItem):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

class Option(TimeStamp):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

class OptionLocalizationItem(LocalizationItem):
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)