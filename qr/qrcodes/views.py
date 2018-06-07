#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from qrcodes.models import Doctor
from qrcodes.models import Vote
import datetime
import qrcode
from qrcode.image.pure import PymagingImage
import plotly.offline as opy
import plotly.graph_objs as go

def human(date):
    return str(date.day).zfill(2) + "." + str(date.month).zfill(2) + "." + str(date.year)


def index(request):
    doctors = Doctor.objects.all()
    return render(request, "index.html", {"doctors": doctors})


def add(request):
    if request.method == "POST":
        doc = Doctor()
        doc.name = request.POST.get("name", "")
        doc.clinic = request.POST.get("clinic", "")
        if doc.name == "" or doc.clinic == "":
            return render(request, "add.html", {})
        doc.save()
        return HttpResponseRedirect("/print/"+str(doc.id))

    return render(request, "add.html", {})


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


def info_view(request, pk):
    doctor = Doctor.objects.get(pk=int(pk))
    x = []
    y = []
    y2 = []
    s = 0
    last_date = ""
    i = 0
    positive = 0
    neutral = 0
    negative = 0
    for vote in Vote.objects.filter(doctor=doctor):
        i+=1
        x.append(i)
        s += vote.vote
        positive += (0,1)[vote.vote == 1]
        neutral += (0,1)[vote.vote == 0]
        negative += (0,1)[vote.vote == -1]
        y.append(s)
        y2.append(vote.vote)

    trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                        mode="lines", name='1st Trace')
    data = go.Data([trace1])
    layout = go.Layout(title=doctor.name, xaxis={'title': 'Время'}, yaxis={'title': 'Рейтинг'})
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    trace2 = go.Scatter(x=x, y=y2, marker={'color': 'red', 'symbol': 100, 'size': "10"},
                        mode="markers", name='2nd Trace')
    data2 = go.Data([trace2])
    layout2 = go.Layout(title=doctor.name, xaxis={'title': 'Время'}, yaxis={'title': 'Отзывы'})
    figure2 = go.Figure(data=data2, layout=layout2)
    div2 = opy.plot(figure2, auto_open=False, output_type='div')

    trace3 = go.Pie(labels=["Хорошие", "Средние", "Плохие"], values=[positive,neutral,negative],
                    hoverinfo='label+percent', textinfo='value',
                    textfont=dict(size=20),
                    marker=dict(colors=["#00ff38", "#fdff00", "#ff008d"],
                                line = dict(color = '#000000', width=1)))
    data3 = go.Data([trace3])
    layout3 = go.Layout(title=doctor.name, xaxis={'title': 'Время'}, yaxis={'title': 'Отзывы'})
    figure3 = go.Figure(data=data3, layout=layout3)
    div3 = opy.plot(figure3, auto_open=False, output_type='div')

    return render(request, "info.html", {"graph": div,
                                         "graph2": div2,
                                         "graph3": div3,
                                         "doctor": doctor, "date": human(datetime.datetime.today())})


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