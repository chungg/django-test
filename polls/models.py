# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Choice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=0)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)

    def __repr__(self):
        return '<%s: %s@%s>' % (self.__class__.name, self.value,
                                self.timestamp)

    def __str__(self):
        return '%s@%s' % (self.value, self.timestamp)
