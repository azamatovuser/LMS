from django.db import models

class TimeStamp(models.Model):
    order = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Course(TimeStamp):
    pass

class CourseLocalizationItem(models.Model):
    course = models.ForeignKey(Course, related_name='course_localization', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    language_type = models.CharField(max_length=50)

class Module(TimeStamp):
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

class ModuleLocalizationItem(models.Model):
    module = models.ForeignKey(Module, related_name='module_localization', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    language_type = models.CharField(max_length=50)

class Lesson(TimeStamp):
    module_id = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)

class LessonLocalizationItem(models.Model):
    module = models.ForeignKey(Lesson, related_name='lesson_localization', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lesson/images/')
    language_type = models.CharField(max_length=50)
    