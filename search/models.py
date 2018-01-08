# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class SearchResultEntry(object):
    def fromDoc(self, doc):
        self.title = doc.attr('@title')
        self.uri = doc.attr('@uri')
        self.mdate = doc.attr('@mdate')
        if doc.texts():
            text = u''
            for t in doc.texts():
                text += t
            self.text = text

@python_2_unicode_compatible  # only if you need to support Python 2
class SearchSet(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    title = models.CharField(max_length=64)
    casket = models.CharField(max_length=128)
    htmltemp = models.CharField(max_length=64)
    snippet_wwidth = models.IntegerField()
    snippet_hwidth = models.IntegerField()
    snippet_awidth = models.IntegerField()
    
    def __str__(self):
        return self.id
