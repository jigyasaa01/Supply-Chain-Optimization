from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.conf import settings
import os
from django.http import FileResponse
import sys
sys.path.append('/path/to/directory')
# from .arima import arima_model
from .SARIMAX import sarimax
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import shutil
from django.views.decorators.csrf import csrf_exempt
import threading
from django.contrib import messages

model_is_done = False
file_path = ''

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            filename = request.FILES['file'].name
            
            # Save the path to the uploaded file in a variable
            global file_path
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            return redirect('use_model')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def show_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    else:
        return render(request, '404.html')

def use_model(request):
    global model_is_done
    model_is_done = False
    def run_model():
        global model_is_done
        # Replace this with your actual model code
        sarimax(file_path)
        model_is_done = True
    # Run the model in a separate thread
    threading.Thread(target=run_model).start()
    # Return the loading page
    return render(request, 'loading.html')

def view_plots(request):
    # Get the list of plots
    plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
    plots = os.listdir(plots_dir)
    plots.sort()
    csv_dir = os.path.join(settings.MEDIA_ROOT, 'csv')
    csv = os.listdir(csv_dir)
    csv.sort()
    # Pass the list of plots and the media URL to the template
    return render(request, 'view_plots.html', {'plots': plots, 'csvs': csv, 'media_url': settings.MEDIA_URL})

def delete_plots(request):
    # Delete all plots
    shutil.rmtree(settings.MEDIA_ROOT)
    os.makedirs(settings.MEDIA_ROOT)
    os.makedirs(settings.MEDIA_ROOT/'plots')
    os.makedirs(settings.MEDIA_ROOT/'csv')
    # Redirect to the 'upload_file' view
    return HttpResponseRedirect(reverse('upload_file'))

def is_model_done(request):
    # Check if the model is done
    if model_is_done:
        return HttpResponse('done')
    else:
        return HttpResponse('not done')


def download_plots(request):
    filename = request.POST['filename']
    # Get the path to the plot
    plot_path = os.path.join(settings.MEDIA_ROOT, 'plots/{filename}'.format(filename=filename))
    if os.path.exists(plot_path):
        response = HttpResponse(open(plot_path, 'rb'), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    else:
        return render(request, '404.html')
    

def download_csv(request):
    filename = request.POST['filename']
    # Get the path to the CSV file
    csv_path = os.path.join(settings.MEDIA_ROOT, 'csv/{filename}'.format(filename=filename))
    print(csv_path)
    if os.path.exists(csv_path):
        response = FileResponse(open(csv_path, 'rb'), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    else:
        return render(request, '404.html')


