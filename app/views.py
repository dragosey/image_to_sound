from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Max

from .forms import ImageUploadForm
from .models import ImageUpload
from .processing import Processing

process = 0
max_id = 0


# Create your views here.
def home(request):
    return render(request, 'index.html')


def home_upload(request):
    global max_id
    if request.method == 'POST':
        form = ImageUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            photos = ImageUpload.objects.all()
            max_id = photos.aggregate(Max('id'))
            max_id = max_id['id__max']
            i = get_object_or_404(ImageUpload, pk=max_id)
            return render(request, 'image.html', {
                    'image_uploaded': i
            })
    return render(request, 'index.html')


def processing(request):
    global process
    process = Processing(max_id)
    process.getRGB()
    return HttpResponse(status=204)


def makefile(request):
    global process
    process.makefile()
    return HttpResponse(status=204)
