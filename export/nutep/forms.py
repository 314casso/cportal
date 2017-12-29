# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from django.utils.encoding import force_text
from django_select2.forms import ModelSelect2Widget


class ContractCustomWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(u'%s %s' % (obj.name, obj.line)).upper()
