from django.db import models
from django.contrib.auth.models import User


class Students(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fname = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)

    gender = models.CharField(max_length=10, choices=[
        ('MALE', 'male'),
        ('FEMALE', 'female'),
        ('OTHER', 'other')
    ])

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