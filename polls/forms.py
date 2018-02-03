from django import forms


class ChoiceForm(forms.Form):
    CHOICES = (('1', '...'), ('2', 'meh'), ('3', 'Ok'),
               ('4', 'Good'), ('5', 'YEAAAAAA'))
    choice_field = forms.ChoiceField(
        label='How you feeling?',  widget=forms.RadioSelect, choices=CHOICES)
