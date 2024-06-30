from django.db import models

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    point_regu = models.IntegerField()

    class Meta:
        db_table = "survey"