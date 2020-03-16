from django.shortcuts import render
from imageai.Detection import ObjectDetection
from django.core.files.storage import FileSystemStorage
from django import forms
import os


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Загрузите изображение', required=True)


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']
            fs = FileSystemStorage()
            name = fs.save(img.name, img)
            context = {
                'file_url': fs.url(name),
                'output_url': fs.url('output.jpg')
            }
            return render(request, 'detect.html', context)

    else:
        form = ImageUploadForm()
    return render(request, 'detect.html', {'form': form})


def object_detect(input_image_path):

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath('/home/kds3000/django_image_ai/resnet50_coco_best_v2.0.1.h5')
    detector.loadModel()
    output_image_path = os.path.join(os.path.dirname(input_image_path), 'output.jpg')
    a_detector = detector.detectObjectsFromImage(input_image=input_image_path,
                                                 output_image_path=output_image_path,
                                                 minimum_percentage_probability=30,
                                                 )
    return output_image_path
