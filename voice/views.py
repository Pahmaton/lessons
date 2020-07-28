from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt
from vosk import Model, KaldiRecognizer
import wave
from django.conf import settings
from .forms import NameForm, VoiceFile
model = Model(settings.BASE_DIR + "/model")


def speech(request):
    result = {
        'имя': None,
        'фамилия': None,
        'отчество': None,
    }
    questions = {
        'первый': None,
    }

    answer=None

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
            res_list = text.split()

            for word in result.keys():
                if word in res_list:
                    result[word] = res_list[res_list.index(word) + 1]
            for word in questions.keys():
                if word in res_list:
                    questions[word] = res_list[res_list.index(word) + 2]

            if questions['первый'] == 'да':
                answer = 2
            if questions['первый'] == 'нет':
                answer = 1
            form=NameForm({
                'last_name': result['фамилия'],
                'first_name': result['имя'],
                'middle_name': result['отчество'],
                'choice': answer
            })

    else:
        form = NameForm()

    return render(request, 'speech/speech.html', context={
        'text': text,
        'form': form
    })


@csrf_exempt
def recognize(request):
    form = VoiceFile(request.POST, files=request.FILES)# заполнить форму из request.POST
    if form.is_valid():# провалидировать
        wf = wave.open(form.cleaned_data['voice'], mode="rb")# получить из формы файл (называется поле voice)
        rec = KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(5000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

        text = json.loads(rec.FinalResult())['text']

    # перевести звук в текст
    # отдать весь текст в полне текст
    return JsonResponse({
        "text": text
    })
