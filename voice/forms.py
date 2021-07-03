from django import forms

class NameForm(forms.Form):
    file = forms.FileField(label="", required=False)

class VoiceFile(forms.Form):
    voice = forms.FileField(label="", required=False)

class RenameFile(forms.Form):
    new_name = forms.CharField(label="Введите новое имя файла", max_length=40)