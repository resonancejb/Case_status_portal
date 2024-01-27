from django import forms
from .models import Case, User

class CaseForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Select Client",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Client'
    )

    class Meta:
        model = Case
        fields = ['case_number', 'parties_involved', 'court_name', 'previous_hearing', 'next_hearing', 'client']

        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Case Number'}),
            'parties_involved': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Parties Involved'}),
            'court_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Court Name'}),
            'previous_hearing': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select Previous Hearing Date'}),
            'next_hearing': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select Next Hearing Date'}),
        }

        labels = {
            'case_number': 'Case Number',
            'parties_involved': 'Parties Involved',
            'court_name': 'Court Name',
            'previous_hearing': 'Previous Hearing Date',
            'next_hearing': 'Next Hearing Date',
        }



class SuperuserEditForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['hearing_date']
        
        widgets = {
            'hearing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select Next Hearing Date'}) 
        }
