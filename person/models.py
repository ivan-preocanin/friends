from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=6, choices=[('male', 'male'), ('female', 'female')], null=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ', id: ' + str(self.id)

