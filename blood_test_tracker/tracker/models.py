from django.db import models

# Create your models here.


class ExamResult(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    data_entrada = models.DateField()
    material = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=100)
    results = models.TextField()
    method = models.CharField(max_length=100)
    reference_value = models.CharField(max_length=100)
    note = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

