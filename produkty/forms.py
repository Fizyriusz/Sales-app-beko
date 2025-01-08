from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        data_rozpoczecia = cleaned_data.get('data_rozpoczecia')
        data_zakonczenia = cleaned_data.get('data_zakonczenia')

        if data_rozpoczecia and data_zakonczenia:
            if data_zakonczenia < data_rozpoczecia:
                raise forms.ValidationError("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.")
        
        return cleaned_data
