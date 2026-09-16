from django.db import models
from django.contrib.auth.models import User


class Students(models.Model):

    # Connect student to Django User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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

    # Email verification status
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + " " + self.sname


class CoursesList(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.course_name


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


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