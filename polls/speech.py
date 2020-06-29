import speech_recognition as sr
import pyaudio


# 51 mic
def show_mics():
    list_mic = sr.Microphone.list_microphone_names()
    for i in range(0, len(list_mic)):
        print(i, list_mic[i])


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=6) as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        a = r.recognize_google(audio, language="ru-RU")
        print("Google thinks you said " + a)
        if a == "на улице дождь":
            print("Нет")
        else:
            print()
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))


if __name__ == '__main__':
    get_audio()
