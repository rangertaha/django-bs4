# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import IndexPageView, FormControlView


urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^form/control$', FormControlView.as_view(), name='form-control'),
    url(r'^form/control$', FormControlView.as_view(), name='form-layout'),
]