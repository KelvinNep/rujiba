from django.db import models

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    pertanyaan1 = models.TextField()
    pertanyaan2 = models.TextField()

    class Meta:
        db_table = "survey"
