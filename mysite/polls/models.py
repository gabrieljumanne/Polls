from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
    # class variable
    question_text = models.CharField("Question Text" ,max_length=200)
    pub_date = models.DateTimeField("date published") # optional human readable name as first postional argument
    
    def __str__(self) -> str:
        return self.question_text
    
    # custom method 
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
    
    
        
class Choice(models.Model):
    #class variable
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Choice Text",max_length=200)
    votes = models.IntegerField( "Votes", default=0)
    
    def __str__(self) -> str:
        return f"{self.choice_text}{self.votes}"