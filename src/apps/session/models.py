from django.db import models
from apps.course.models import Course, Lesson, Module
from apps.quiz.models import Option, Quiz
from apps.account.models import User

class Status(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"
    COMPLETED = "completed", "Completed"

class TimeStamp(models.Model):
    status = models.CharField(max_length=20, choices=Status, default=Status.CLOSED)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class UserCourseSession(TimeStamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

class UserModuleSession(TimeStamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.FloatField()

class UserLessonSession(TimeStamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class UserAnswerSession(TimeStamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct = models.IntegerField()
    not_correct = models.IntegerField()

class Answer(TimeStamp):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)
    