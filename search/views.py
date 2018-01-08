# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404

import estraier_c as est_c
import models
import forms

def index(request, setid):
    sset = get_object_or_404(models.SearchSet, id=setid)
    form = forms.QueryForm(request.GET)
    status = 200
    entryPerPage = 10
    fromIndex = 1
    context = {
        'setid': setid,
        'title': sset.title,
        'form': form,
    }
    cond = est_c.Condition()
    phrase = None
    if form.is_valid():
        phrase = form.cleaned_data['q']
        cond.set_phrase(phrase)
        fromIndex = form.cleaned_data['start']
        if not fromIndex:
            fromIndex = 1
        cond.set_skip(fromIndex - 1)
        cond.set_order(form.cleaned_data['order'])
    context['start'] = fromIndex
    db = est_c.Database()
    if not db.open(sset.casket, est_c.Database.DBREADER):
        errno = db.error()
        context['error'] = db.err_msg(errno)
        status = 500
    elif phrase:
        r = db.search(cond)
        result = []
        for i in range(10):
            id = r.get_doc_id(i)
            if id != -1:
                doc = db.get_doc(id, 0)
                item = models.SearchResultEntry()
                item.fromDoc(doc)
                result.append(item)
        hitnum = int(r.hint(''))
        context['hitnum'] = hitnum
        context['result'] = result
        if fromIndex >= entryPerPage:
            p = request.GET.copy()
            if 'start' in p:
                del p['start']
            p.update({'start': fromIndex - entryPerPage})
            context['param_prev'] = p.urlencode()
        if (fromIndex + entryPerPage) < hitnum:
            p = request.GET.copy()
            if 'start' in p:
                del p['start']
            p.update({'start': fromIndex + entryPerPage})
            context['param_next'] = p.urlencode()
        context['doc_num'] = db.doc_num()
    db.close()
    return render(request, 'search/index.html', context, status=status)
