from django.contrib import admin
from django import forms
import json

from .models import Portfolio


class PortfolioAdminForm(forms.ModelForm):
    tech = forms.CharField(
        widget=forms.Textarea(attrs={"rows":4}),
        required=False,
        help_text='Enter a JSON array (e.g. ["React", "Django"]) or a comma-separated list (e.g. React, Django).'
    )
    url = forms.URLField(help_text='Include the scheme, e.g. https://example.com')

    class Meta:
        model = Portfolio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show a friendly, editable representation of the tech list
        if self.instance and getattr(self.instance, 'tech', None):
            tech_value = self.instance.tech
            if isinstance(tech_value, (list, tuple)):
                self.fields['tech'].initial = ', '.join(map(str, tech_value))
            else:
                self.fields['tech'].initial = str(tech_value)

    def clean_tech(self):
        val = (self.cleaned_data.get('tech') or '').strip()
        if not val:
            return []
        # If it looks like JSON, try to parse it
        if val.startswith('['):
            try:
                parsed = json.loads(val)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f'Invalid JSON array: {e}')
            if not isinstance(parsed, list):
                raise forms.ValidationError('JSON must be an array/list.')
            return parsed
        # Otherwise treat as comma-separated
        items = [s.strip() for s in val.split(',') if s.strip()]
        return items


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    form = PortfolioAdminForm
    list_display = ('name', 'category', 'url', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'tech')
