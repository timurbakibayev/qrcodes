from django.shortcuts import render
from qrcodes.models import Doctor


def doc_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    return render(request, "doc_vote.html", {"doctor": doctor})