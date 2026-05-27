from django import forms
from .models import Page, Section


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'section', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок сторінки'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'url-назва'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'slug', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва розділу'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пошук по вікі...',
        })
    )
