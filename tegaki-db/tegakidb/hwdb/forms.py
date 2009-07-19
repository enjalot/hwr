#from django import forms
from dojango import forms

from tegakidb.users.models import TegakiUser
from django.contrib.auth.models import User
from tegakidb.hwdb.models import *

#form for editing tegaki users
class CharacterSetForm(forms.ModelForm):
    #name = forms.CharField(max_length=30)
    lang = forms.fields.ModelChoiceField(queryset=Language.objects.all(), label="Language")
    #description = forms.CharField(max_length=255)
    #characters = forms.TextField()
    #public = forms.BooleanField(default=True)
    class Meta:
        model = CharacterSet
        exclude = ('id','user_id', 'user_display')

    #def __init__(self, *args, **kwargs):
    #    super(CharacterSetForm, self).__init__(*args, **kwargs)
    #    self.fields['lang'] = forms.fields.ModelChoiceField(queryset=Language.objects.all(), label="Language")
        #try:
        #    self.fields['lang'].label = "Language"
        #except:
        #    pass

    def save(self, commit=True):
        m = super(CharacterSetForm, self).save(commit=False)
        m.lang = self.cleaned_data['lang'].subtag
        if commit:
            m.save()
        return m

    #def clean_lang(self):
    #    l = self.cleaned_data['lang']
    #    print l
    #    return l



