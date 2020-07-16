from django.shortcuts import render
from subprocess import run, PIPE
import sys

def button(request):
    return render(request, 'home.html')

def output(request):
    data = 'Hello world'
    print(data)
    return render(request, "home.html", {'data':data})

def external(request):
    inp_type=request.POST.get("param")
    inp_filename = request.POST.get("filename")
    inp_output = request.POST.get("output")
    inp_spreadsheetid = request.POST.get("gsid")
    inp_worksheet = request.POST.get("wks")
    inp_creds = request.POST.get("creds")




    out=run([sys.executable, './run_qrcgeneration.py',
             "-t", inp_type,
             "-f", inp_filename,
             "-o", inp_output,
             "-s", inp_spreadsheetid,
             "-w", inp_worksheet,
             "-j", inp_creds], shell=False, stdout=PIPE, text=True)
    print(out)

    return render(request, 'home.html', {'data1':out.stdout})
