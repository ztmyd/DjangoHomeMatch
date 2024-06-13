from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from home_match.models import CustomUser, Property, Incident
from .models import Property

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BasicPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'sale_or_rent', 'zone', 'price', 'number_of_rooms', 'property_type', 'image']

class DetailedPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['description', 'size', 'number_of_bathrooms', 'number_of_parking_spaces', 'status', 'maintenance_fee', 'number_of_elevators', 'floor', 'accepts_pets', 'social_area', 'address', 'link', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8']

class PropertyFilterForm(forms.Form):
    sale_or_rent = forms.ChoiceField(choices=[('sale', 'Venta'), ('rent', 'Alquiler')], required=False)
    zone = forms.ChoiceField(choices=[('central', 'Zona Céntrica'), ('south', 'Zona Sur'), ('north', 'Zona Norte')], required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    property_type = forms.ChoiceField(choices=[('house', 'Casa'), ('apartment', 'Departamento')], required=False)
    number_of_rooms = forms.IntegerField(required=False)

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['description']
        labels = {'description': 'Descripción del Incidente'}

class BankTransferForm(forms.Form):
    account_number = forms.CharField(max_length=100, label='Número de Cuenta')
    bank_name = forms.CharField(max_length=100, label='Nombre del Banco')
    swift_code = forms.CharField(max_length=100, label='Código SWIFT')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Monto')