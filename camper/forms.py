from django import forms
from .models import Camper

class CamperForm(forms.ModelForm):
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')

    class Meta:
        model = Camper
        fields = ['first_name', 'last_name','gender','date_of_birth','email','phone','different_class', 'created_by']

        labels = {
            # 'different_class': 'Different Classes'
            # 'date_of_birth': 'Date of birth (YYYY-MM-DD)'
        }

    def __init__(self, *args, **kwargs):
        super(CamperForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select'
        self.fields['different_class'].empty_label = 'Select'
        