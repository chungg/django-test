# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.views.generic import edit

from . import forms


class VoteView(edit.FormView):
    form_class = forms.ChoiceForm
    template_name = 'polls/vote.html'
    success_url = '/polls/results'


class ResultsView(generic.TemplateView):
    template_name = 'polls/results.html'
