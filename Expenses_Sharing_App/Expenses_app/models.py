from django.db import models

# Create your models here.

class Expense(models.Model):
    from_id = models.IntegerField(null=False)
    to_id = models.IntegerField(null=False)
    status = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    