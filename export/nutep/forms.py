# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm
from django.utils.encoding import force_text
from django_select2.forms import ModelSelect2Widget

from nutep.models import Contract, UploadedTemplate


class ContractCustomWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(u'%s %s' % (obj.name, obj.line)).upper()


class TemplateForm(ModelForm):
    contract = forms.ModelChoiceField(label=u"Договор", queryset=Contract.objects.all(),
                                      widget=ContractCustomWidget(
                                          attrs={'style': 'width:100%', 'required': None}))
    attachment = forms.FileField(label=u"Шаблон", widget=forms.FileInput(
        attrs={'class': 'fileupload', 'required': None}))
#     is_override = forms.BooleanField(label=u"Режим замещения", widget=forms.CheckboxInput(
#         attrs={'class': 'flat'}), initial=False, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['contract'].widget.queryset = Contract.objects.for_user(
            user)

    class Meta:
        model = UploadedTemplate
        fields = ['contract', 'attachment']
