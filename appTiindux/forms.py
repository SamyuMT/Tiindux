from django import forms
from .models import DatabaseConnection

class DatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = ['user', 'password']
