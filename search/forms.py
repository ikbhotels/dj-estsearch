# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

order_choices = (
    (u'', u'スコア順'),
    (u'@mdate NUMD', u'新→旧'),
    (u'@mdate NUMA', u'旧→新'),
)

class QueryForm(forms.Form):
    q = forms.CharField()
    order = forms.ChoiceField(choices=order_choices, required=False)
    start = forms.IntegerField(required=False)
