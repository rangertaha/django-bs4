# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import FormControlForm

class IndexPageView(TemplateView):
    template_name = 'demo/form.html'


class FormControlView(FormView):
    template_name = 'demo/form-control.html'
    form_class = FormControlForm
