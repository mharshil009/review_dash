from django.db import models

class Review(models.Model):
    review_id = models.CharField(max_length=100, unique=True)
    reviewer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateField()

    sentiment = models.CharField(max_length=10, choices=[
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative')
    ], blank=True)

    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.review_id} - {self.reviewer_name}'
