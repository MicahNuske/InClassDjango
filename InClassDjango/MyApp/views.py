from http.client import HTTPResponse
from tkinter import Canvas
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from MyApp.models import teacher
from .forms import InputForm

from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from io import BytesIO


# Create your views here.
def index(request):
    
    teach = teacher.objects.all()
    return render(request, "MyApp/index.html", {'content' :teach})


def input_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = InputForm()

    return render(request, "MyApp/input.html", {"form": form})

def delete(request, id):
    Teacher = teacher.objects.get(id=id)
    Teacher.delete()
    return HttpResponseRedirect(reverse('index'))

def report(request):
    pdf_file = staticfiles_storage.path("DS.pdf")

    try:
        merger = PdfWriter()

        input1 = PdfReader(generate_pdf())
        input2 = PdfReader(pdf_file, "rb")

        merger.append(input1)
        merger.append(input2)

        buffer = BytesIO()
        merger.write(buffer)

        buffer.seek(0)

        response = FileResponse(buffer, as_attachment=True, filename="Attachment.pdf")
#find a way to use python to give it a unique name


    except FileNotFoundError:
        response = FileResponse(generate_pdf(), as_attachment=True, filename="noAttachment.pdf")

    return response

def generate_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    lines = [('Name:', 'Teaching Area:')]

    teachers = teacher.objects.all()

    for teach in teachers:
        lines.append((teach.Name, teach.Area))

    table = Table(lines)
    table.wrapOn(p, 300, 300)
    table.drawOn(p, 10, 600)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
#might be a better way to do this
