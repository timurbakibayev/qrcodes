from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=1000)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.clinic) + ": " + self.name


class Vote(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=1000)
    vote = models.IntegerField(default=3)
    comment = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.doctor) + " vote " + str(self.vote)
