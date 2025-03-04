from django.db import models
from django.contrib.auth import get_user_model
from users.models import Instructor  


User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    accessibility_options = models.JSONField(default=list)  # Store options like ["audio_description", "closed_captions"]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"