from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Question(models.Model):

    question_text = models.CharField("Question Text" ,max_length=200)
    pub_date = models.DateTimeField("date published") # optional human readable name as first postional argument
    publisher = models.CharField("publisher", max_length=250, default = 'Unknown')

    def __str__(self) -> str:
        return self.question_text
    
    # custom functionality 
    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now 


    def was_published_by(self):
        return{
            'question':self.question_text,
            'pub_date':self.pub_date,
            'publisher': self.publisher
        }
    
        
class Choice(models.Model):
    #class variable
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Choice Text",max_length=200)
    votes = models.IntegerField( "Votes", default=0)
    
    def __str__(self) -> str:
        return f"{self.choice_text}{self.votes}"