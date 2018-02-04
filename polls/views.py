# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools

from django import shortcuts as sc
from django.views import generic
from django.views.generic import edit
import numpy

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

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        groups = [i[0] for i in
                  self.request.user.groups.all().values_list('id')]
        matches = (models.Choice.objects.filter(user__groups__in=groups).all()
                   if groups else models.Choice.objects.all())
        matches = [i[0] for i in matches.values_list('value')]
        context['avg_score'] = numpy.mean(matches) if matches else 0.0
        values, texts = zip(*models.Choice.CHOICES)
        context['score_count'] = list(itertools.izip_longest(
            texts, values, numpy.bincount(matches)[1:], fillvalue=0))
        return context
