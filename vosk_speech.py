#!/usr/bin/env python3
import math
import struct
import audioop
from time import sleep

from vosk import Model, KaldiRecognizer


import pyaudio

model = Model("vosk-model-small-ru-0.4")
rec = KaldiRecognizer(model, 16000)

Threshold = 400

SHORT_NORMALIZE = (1.0/32768.0)

sample_width = 16000

def get_audio():
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index=6, format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    frames = []
    cnt = 0
    print('start')
    sleep(1)
    while True:
        if cnt >= 50:
            break
        cnt += 1
        data = stream.read(4000)
        frames.append(data)
        # if audioop.rms(data, sample_width) > Threshold:
        #     break
    frames = [f for f in frames if f]
    for frame in frames:
        if rec.AcceptWaveform(frame):
            print(rec.Result())
        else:
            print(rec.PartialResult())



CHUNK = 1024




def get_audio_v2():
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index=6, format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNK)

    elapsed_time = 0
    seconds_per_buffer = float(CHUNK) / sample_width
    pause_buffer_count = int(math.ceil(0.8 / seconds_per_buffer))
    frames = []

    print('start')
    while True:
        elapsed_time += seconds_per_buffer
        data = stream.read(CHUNK)
        if audioop.rms(data, 2) > Threshold:
            frames.append(data)
            break

    pause_count, phrase_count = 0, 0
    phrase_time_limit = 5
    phrase_start_time = elapsed_time
    while True:
        elapsed_time += seconds_per_buffer
        if phrase_time_limit and elapsed_time - phrase_start_time > phrase_time_limit:
            break

        buffer = stream.read(CHUNK)
        if len(buffer) == 0:
            break

        energy = audioop.rms(buffer, 2)  # unit energy of the audio signal within the buffer
        if energy > Threshold:
            frames.append(buffer)
            pause_count = 0
        else:
            pause_count += 1
        if pause_count > pause_buffer_count:
            break

    for frame in frames:
        if rec.AcceptWaveform(frame):
            print(rec.Result())
        else:
            print(rec.PartialResult())


if __name__ == '__main__':
    roms()
