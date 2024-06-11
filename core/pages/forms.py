from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from .models import Hosts

class CreateForm(forms.ModelForm):
    class Meta:
        model = Hosts
        fields = ['hostname','host_type','mac_1','mac_2']
        widgets = {
                'mac_1': forms.TextInput(attrs={'oninput': 'addColon(this)', 'maxlength': '5'})
        }

    def save(self,commit=True):
        instance=super().save(commit=False)
        if not instance.mac_2:
            instance.mac_2='-'
        if commit:
            instance.save()
        return instance



class UnwForm(forms.ModelForm):
    class Meta:
        model=Hosts
        fields=['hostname','host_type']