from django.db import transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from catalog.models import Product, Version


class CombinedProductVersionForm(forms.ModelForm):
    version_number = forms.CharField(max_length=50)
    version_name = forms.CharField(max_length=100)
    is_current_version = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def __init__(self, *args, **kwargs):
        super(CombinedProductVersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('is_current_version', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'description',
            'image',
            'price',
            Row(
                Column('version_number', css_class='form-group col-md-6 mb-0'),
                Column('version_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить', css_class='btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for forbidden_word in forbidden_words:
            if forbidden_word in name:
                self.add_error('name', 'В названии продукта обнаружено запрещенное слово.')
            if forbidden_word in description:
                self.add_error('description', 'В описании продукта обнаружено запрещенное слово.')

    @transaction.atomic
    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            Version.objects.create(
                product=product,
                version_number=self.cleaned_data['version_number'],
                version_name=self.cleaned_data['version_name'],
                is_current_version=self.cleaned_data['is_current_version']
            )
        return product



class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
