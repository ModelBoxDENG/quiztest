from django.db import models

# Create your models here.

class Quiz:
    question_id = models.AutoField(primary_key = True)
    question = models.CharField(max_length=250)
    response = models.CharField(max_length=500)#['r1','r2','r3','r4']

    def __str__(self):
        return self.quiz_text
        

class User(models.Model):
    name = models.CharField(max_length = 32);
    finished_question= models.CharField(max_length = 500);
    
    def __str__(self):
        return self.user_text

    
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=0)

    def __str__(self):
        return self.choice_text

