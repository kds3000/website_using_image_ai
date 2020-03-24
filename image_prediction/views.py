from django.shortcuts import render
from imageai.Prediction import ImagePrediction
from django.core.files.storage import FileSystemStorage
from django import forms
from translate import Translator


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Загрузите изображение', required=True)


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']
            fs = FileSystemStorage()
            name = fs.save(img.name, img)
            probs = image_predict(img)
            context = {
                'probs': probs,
                'file_url': fs.url(name),
            }
            return render(request, 'predict.html', context)
    else:
        form = ImageUploadForm()
    return render(request, 'predict.html', {'form': form})


def image_predict(image):

    prediction = ImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("/home/kds3000/django_image_ai/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
    prediction.loadModel()

    predictions, probabilities = prediction.predictImage(image, result_count=5)
    output_dict = {}
    translator = Translator(to_lang="ru")
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        converted_prob = convert_probability(eachProbability)
        translated_name = translator.translate(eachPrediction.replace('_', ' '))
        output_dict[translated_name] = converted_prob
    return output_dict


def convert_probability(prob):
    if prob <= 0.05:
        return "менее 0.01 %"
    return '{} %'.format(round(prob, 2))

