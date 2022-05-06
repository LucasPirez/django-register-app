from ast import Delete
from calendar import day_abbr
from pyexpat import model
from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import DurationField

# Create your models here.

class User(AbstractUser):
    pass
    feePaid = models.BooleanField(default=False)


class Day(models.Model):
    dayClass = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.dayClass}" 


class Professor(models.Model):
    professorName= models.CharField(max_length=64)
 


    def __str__(self):
        return f"{self.professorName}" 

class ClassName(models.Model):
     nameClass = models.CharField(max_length=64)
     classHour = models.TimeField()
     duration = models.IntegerField(null=True)
     asignacion = models.ManyToManyField(Day, related_name="asig")
     profer = models.ForeignKey(Professor, on_delete=models.CASCADE,default=1 )
     student = models.ManyToManyField(User, related_name='stu', )
     codeTime = models.IntegerField(null=True)


     def __str__(self):
        return f"{self.nameClass}    {self.classHour}" 

     def serialize(self):
        return {
            "id": self.id,
            "nameClass": self.nameClass,
            "duration": self.duration,
            "classHour": self.classHour,
            "student": [date.username for date in self.student.all()],
            "asignacion": [dat.dayClass for dat in self.asignacion.all()],
            "codeTime": self.codeTime
        }
        
class Comment(models.Model):
    newComment = models.CharField(max_length=250)
    motive = models.CharField(max_length=54,default=1)
    authorComment = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    timeComment = models.DateField()

    def __str__(self):
        return f"{self.authorComment} {self.timeComment}" 

class Questions(models.Model):
    quest = models.CharField(max_length=100)
    answer = models.CharField(max_length=350)

        
    
    def serialize(self):
        return {
            "id": self.id,
            "quest": self.quest,
            "answer": self.answer,
        }