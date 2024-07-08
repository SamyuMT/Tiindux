from django.db import models

class DatabaseConnection(models.Model):
    host = "162.241.91.186"
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    database = "data360tiindux_bdfumdir"
    def __str__(self):
        return f"{self.user}@{self.host}/{self.database}"