from django.db import models
import datetime

class ClusterData(models.Model):
    cluster_name = models.CharField(max_length=300)
    bucket_name = models.CharField(max_length=300)
    #date = models.DateTimeField()
    cloud_account = models.CharField(max_length=300)
    date = datetime.datetime.now().strftime ("%Y-%m-%d")
    class Meta:
        db_table='clusters'

    def __str__(self):
        return self.cluster_name
