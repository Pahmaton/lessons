from django import forms

class NameForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=100, required=False)
    first_name = forms.CharField(label='Имя', max_length=100, required=False)
    middle_name = forms.CharField(label='Отчество', max_length=100, required=False)
    choice = forms.ChoiceField(label="Вы когда-нибудь болели?", required=False, choices=(
        (0, ("Выберите ответ")),
        (1, ("Нет")),
        (2, ("Да")),
    ))
    file = forms.FileField(label="", required=False)

class VoiceFile(forms.Form):
    voice = forms.FileField(label="", required=False)
