from django import forms

from .models import CATEGORY_COLOR_CHOICES, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'type', 'color')
        labels = {
            'name': 'Nome da categoria',
            'type': 'Tipo',
            'color': 'Cor',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'type': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
            'color': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 text-white'}),
        }

    def clean_color(self):
        color = self.cleaned_data.get('color')
        valid_colors = {choice[0] for choice in CATEGORY_COLOR_CHOICES}
        if color not in valid_colors:
            raise forms.ValidationError('Selecione uma cor válida.')
        return color
