# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django import shortcuts as sc
from django.views import generic
from django.views.generic import edit

from . import forms, models


class VoteView(edit.FormView):
    form_class = forms.ChoiceForm
    template_name = 'polls/vote.html'
    success_url = '/polls/results'

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.utcnow()
        tomorrow = now + datetime.timedelta(days=1)
        if models.Choice.objects.filter(timestamp__gte=now.date(),
                                        timestamp__lt=tomorrow.date(),
                                        user=request.user).exists():
            return sc.redirect('/polls/results')
        return super(VoteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        resp_obj = models.Choice(value=int(form.cleaned_data['choice_field']),
                                 user=self.request.user)
        resp_obj.save()
        return super(VoteView, self).form_valid(form)


class ResultsView(generic.TemplateView):
    template_name = 'polls/results.html'
