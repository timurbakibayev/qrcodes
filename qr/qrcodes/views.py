from django.shortcuts import render
from qrcodes.models import Doctor
from qrcodes.models import Vote
import datetime


def human(date):
    return str(date.day).zfill(2) + "." + str(date.month).zfill(2) + "." + str(date.year)


def vote_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    return render(request, "doc_vote.html", {"doctor": doctor, "date": human(datetime.datetime.today()) })


def vote_done_view(request, pk, vote):
    doctor = Doctor.objects.get(pk=int(pk))
    vote = int(vote)-2
    my_vote = Vote()
    my_vote.doctor = doctor
    my_vote.vote = vote
    my_vote.comment = "No comments"
    my_vote.save()

    return render(request, "doc_vote_done.html", {"doctor": doctor, "date": human(datetime.datetime.today()),
                                                  "my_vote": my_vote, "votes": Vote.objects.filter(doctor_id=pk)})