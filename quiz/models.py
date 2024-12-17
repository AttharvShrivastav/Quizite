# quiz/models.py
from django.db import models

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# class Leaderboard(models.Model):
#     user = models.CharField(max_length=255)
#     score = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.score}"
