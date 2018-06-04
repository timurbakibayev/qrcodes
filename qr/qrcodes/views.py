from django.shortcuts import render, HttpResponse
from qrcodes.models import Doctor
from qrcodes.models import Vote
import datetime
import qrcode
from qrcode.image.pure import PymagingImage

def human(date):
    return str(date.day).zfill(2) + "." + str(date.month).zfill(2) + "." + str(date.year)


def index(request):
    doctors = Doctor.objects.all()
    return render(request, "index.html", {"doctors": doctors})


def add(request):
    doctors = Doctor.objects.all()
    return render(request, "add.html", {"doctors": doctors})


def qr_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    img = qrcode.make('http://qrvote.kz/vote/'+str(doctor.id), image_factory=PymagingImage, version=3, border = 2,
                      error_correction=qrcode.constants.ERROR_CORRECT_L,
                      box_size=10)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def vote_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    return render(request, "doc_vote.html", {"doctor": doctor, "date": human(datetime.datetime.today()) })


def print_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    return render(request, "print.html", {"doctor": doctor, "date": human(datetime.datetime.today())})


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