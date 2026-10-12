from django import forms
from .models import Resume, Education, Experience, Skill, Language, Certification, Reference, Hobby

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['template', 'photo', 'full_name', 'email', 'phone', 'address', 'summary']
        widgets = {
            'template': forms.HiddenInput(),
            'full_name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'address': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'summary': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'rows': 4}),
        }



class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'qualification', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'qualification': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'rows': 3}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'company': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'rows': 3}),
        }



class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'placeholder': 'e.g. Project Management'}),
            'proficiency': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'placeholder': 'e.g. Spanish'}),
            'proficiency': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['title', 'issuer', 'date_awarded']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'issuer': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'date_awarded': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2'}),
        }


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['name', 'relationship', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'relationship': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'placeholder': 'e.g. Former Manager'}),
            'contact': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'placeholder': 'Email or phone'}),
        }


class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'placeholder': 'e.g. Chess, Hiking, Photography'}),
        }