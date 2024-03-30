from django import forms
from .models import *

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['assigned_to', 'created_by',]
