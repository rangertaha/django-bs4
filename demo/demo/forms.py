# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils.translation import ugettext as _


from bs4.tests import TestForm

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)
STATUS_CHOICES = (
    (1, _("Not relevant")),
    (2, _("Review")),
    (3, _("Maybe relevant")),
    (4, _("Relevant")),
    (5, _("Leading candidate"))
)
RELEVANCE_CHOICES = (
    (1, _("Unread")),
    (2, _("Read"))
)


'''
class FormControlForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class CViewerForm(forms.Form):
    status = forms.ChoiceField(choices = STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)
    relevance = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True)

'''
BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)
CHOICES = (('1', 'First',), ('2', 'Second',))

class FormControlForm(forms.Form):

    email = forms.EmailField(label='Email address', required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    input = forms.CharField(label='Text input', max_length=100)
    number = forms.IntegerField(label='Select number', max_value=100)
    multi_select = forms.IntegerField(label='Select multiple numbers', max_value=100)

    '''
    select = forms.
    multi_select
    boolean
    date = forms.DateField()
    image = forms.ImageField()
    text = forms.FileField(required=False)
    '''


    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)


    forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    url = forms.URLField()

    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))


