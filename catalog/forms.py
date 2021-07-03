from django import forms

class ThimbleForm(forms.Form):
    thimble_form_name = forms.CharField(label='Введите имя:', max_length=200)