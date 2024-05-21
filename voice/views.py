from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect
import json
import time
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from vosk import Model, KaldiRecognizer
import wave
from django.conf import settings
from .forms import NameForm, VoiceFile, RenameFile
from .models import AudioFile
model = Model(settings.BASE_DIR + "/model")

def speech(request):
    text=None

    if request.method == "POST":
        form = NameForm(request.POST, files=request.FILES)
        if form.is_valid():
            wf = wave.open(form.cleaned_data['file'], mode="rb")

            rec = KaldiRecognizer(model, wf.getframerate())

            while True:
                data = wf.readframes(5000)
                if len(data) == 0:
                    break
                rec.AcceptWaveform(data)

            text = json.loads(rec.FinalResult())['text']

    else:
        form = NameForm()

    return render(request, 'speech/speech.html', context={
        'text': text,
        'form': form
    })

@csrf_exempt
def recognize(request):
    form = VoiceFile(request.POST, files=request.FILES)
    if form.is_valid():
        wf = wave.open(form.cleaned_data['voice'], mode="rb")
        rec = KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(5000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

        text = json.loads(rec.FinalResult())['text']

        if text == '':
            file_name = 'Пустое название'
            text = 'Текст пуст, потому что вы ничего не сказали'
            real_file_name = ''
        else:
            text_list = text.split()
            real_file_name = text.capitalize() + '.'
            if len(text_list) > 3:
                joiner = (text_list[0], '', text_list[1], '', text_list[2] + '...')
                capital = (' '.join(joiner))
                file_name = capital.capitalize()
                text = text.capitalize()
                result = list(text)
                if len(result) > 49:
                    result = list(text)
                    result3 = result[0:49]
                    result6 = ''.join(result3)
                    result4 = result6.split()
                    result4.pop()
                    result7 = ' '.join(result4)
                    text = result7 + '...'
                else:
                    text = text + '.'
            else:
                joiner = text + '.'
                text = text + '.'
                file_name = joiner.capitalize()
                text = text.capitalize()

        time_now = time.ctime()
        time_now_list = time_now.split()
        day = time_now_list[2]
        month = time_now_list[1]
        day_of_week = time_now_list[0]
        year = time_now_list[4]
        clock = time_now_list[3]
        month_list_ru = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября",
                         "Октября", "Ноября", "Декабря"]
        month_list_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        dow_list_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        dow_list_en = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        index_dow = dow_list_en.index(day_of_week)
        index_mouth = month_list_en.index(month)
        file_time_pre = (day, month_list_ru[index_mouth] + ',', dow_list_ru[index_dow] + ',', year, "год" + ',', clock)
        file_time = ' '.join(file_time_pre)

        a = AudioFile(text=text, files=form.cleaned_data['voice'], file_name=file_name, file_time=file_time,
                      real_file_name=real_file_name)
        a.save()
    return JsonResponse({
        "text": text
    })


def my_files(request):
    context = {
        'files': AudioFile.objects.all(),
        'form': RenameFile()
    }
    return render(request, 'speech/audio_files.html', context)

def del_files(request, file_id):
    b = AudioFile.objects.get(id=file_id)
    b.delete()
    return redirect(reverse('voice:my_files'))

def tutorial(request):
    return render(request, 'speech/tutorial.html')

def files_info(request, file_id):
    context = {
        'files_info': AudioFile.objects.get(id=file_id)
    }
    return render(request, 'speech/files_info.html', context)

@csrf_exempt
def files_rename(request, file_id):
    form = RenameFile(request.POST or None)
    if form.is_valid():
        c = AudioFile.objects.get(id=file_id)
        c.file_name = form.cleaned_data['new_name']
        c.save()

    return render(request, 'speech/audio_files.html', context={
        'form': form,
        'files': AudioFile.objects.all()
    })
