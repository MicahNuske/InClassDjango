from django.db import models

# Create your models here.
class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)

class course(models.Model):
    CourseT = models.CharField(max_length=135)
    UnitT = models.CharField(max_length = 30)
    UnitVal = models.CharField(max_length = 20)

class assess(models.Model):
    Items = models.CharField(max_length = 125)
    Weight = models.CharField(max_length = 5)
    StartDate = models.CharField(max_length = 20)
    DueDate = models.CharField(max_length = 20)
