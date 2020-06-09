from django.db import models
import datetime

class ClusterData(models.Model):
    cluster_name = models.CharField(max_length=300)
    bucket_name = models.CharField(max_length=300)
    #date = models.DateTimeField()
    date = datetime.datetime.now().strftime ("%Y-%m-%d")
    class Meta:
        db_table='clusters'
