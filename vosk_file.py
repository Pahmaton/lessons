import json
from nltk.corpus import stopwords

from python_speech_features import mfcc
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import re

SetLogLevel(0)

#if not os.path.exists("model"):
   # print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
   # exit (1)


wf = wave.open('example.wav', mode="rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(5000)
    if len(data) == 0:
        break
    rec.AcceptWaveform(data)


def question():
    result = {
        'имя': None,
        'фамилия': None,
        'отчество': None
    }
    text = json.loads(rec.FinalResult())['text']
    res_list = text.split()
    print(res_list)

    for word in result.keys():
        if word in res_list:
            result[word] = res_list[res_list.index(word)+1]
    print(result)

print(stopwords.words("english"))
question()

# r'.* имя (\w) .*'
# r'.* фамилия (\w) .*'
# r'.* отчество (\w) .*'
# "vое имя андрей, а фамилия зданчук фвдфоловфы отчество иванович"