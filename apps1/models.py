from django.db import models
from django.contrib.auth.models import User


# Independent student model
class Students(models.Model):

    fname = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    email = models.EmailField()

    gender = models.CharField(
        max_length=10,
        choices=[
            ('MALE', 'male'),
            ('FEMALE', 'female'),
            ('OTHER', 'other')
        ]
    )

    dob = models.DateField()

    contact_number = models.CharField(max_length=15)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    hobbies = models.JSONField(default=list)

    image = models.ImageField(
        upload_to="documents/",
        blank=True,
        null=True
    )

    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.fname + " " + self.sname


# Available courses
class CoursesList(models.Model):

    course_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.course_name


# User's additional profile
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# Course enrollment
class CourseEnrollment(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course = models.ForeignKey(
        CoursesList,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} - {self.course}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
