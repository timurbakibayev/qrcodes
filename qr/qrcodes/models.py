from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=1000)
    clinic = models.CharField(max_length=1000, default="Поликлиника")

    def avg(self):
        votes = [(vote.vote+1)*2.5 for vote in Vote.objects.filter(doctor=self)]
        if len(votes) > 0:
            return str(int(sum(votes)/len(votes)))+ "."+ str(int(sum(votes)/len(votes)*10)%10)
            # return sum(votes)/len(votes)
        return 0

    def __str__(self):
        return str(self.clinic) + ": " + self.name


class Vote(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=1000)
    vote = models.IntegerField(default=3)
    comment = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.doctor) + " vote " + str(self.vote)
