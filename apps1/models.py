from django.db import models

# Create your models here.
class Hobby(models.Model):
    name = models.CharField(max_length=100)

class Students(models.Model):

# columns-

    fname=models.CharField(max_length=100)
    sname=models.CharField(max_length=100)
    gender=models.CharField(choices=[('MALE','male'),
                     ('FEMALE','female'),
                     ('OTHER','other')])
    dob=models.DateField()
    email=models.EmailField(unique=True)
    contact_number=models.CharField()
    age=models.IntegerField()
    hobbies = models.JSONField(default=list)
    # country,state,city Dropdown !!!
    image=models.ImageField(upload_to="documents/")

    

