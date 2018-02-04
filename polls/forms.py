from django import forms

from . import models


class ChoiceForm(forms.Form):
    choice_field = forms.ChoiceField(
        label='How you feeling?',  widget=forms.RadioSelect,
        choices=models.Choice.CHOICES)
