from datetime import datetime, timezone
from decimal import Decimal
from io import BytesIO
import uuid
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Incident, Property
from .forms import BankTransferForm, BasicPropertyForm, CustomUserCreationForm, DetailedPropertyForm, IncidentForm, PropertyFilterForm
from xhtml2pdf import pisa

def home(request):
    properties = Property.objects.all()
    if request.method == 'GET':
        form = PropertyFilterForm(request.GET)
        if form.is_valid():
            sale_or_rent = form.cleaned_data.get('sale_or_rent')
            zone = form.cleaned_data.get('zone')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            property_type = form.cleaned_data.get('property_type')
            number_of_rooms = form.cleaned_data.get('number_of_rooms')
            
            if sale_or_rent:
                properties = properties.filter(sale_or_rent=sale_or_rent)
            if zone:
                properties = properties.filter(zone=zone)
            if min_price is not None:
                properties = properties.filter(price__gte=min_price)
            if max_price is not None:
                properties = properties.filter(price__lte=max_price)
            if property_type:
                properties = properties.filter(property_type=property_type)
            if number_of_rooms:
                properties = properties.filter(number_of_rooms=number_of_rooms)
    else:
        form = PropertyFilterForm()

    return render(request, 'home.html', {'form': form, 'properties': properties})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('custom_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = BasicPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)  
            property.user = request.user  
            property.save()  
            return redirect('add_property_details', property_id=property.id)
    else:
        form = BasicPropertyForm()
    return render(request, 'add_property.html', {'form': form})

@login_required
def add_property_details(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = DetailedPropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_detail', property_id=property.id)
    else:
        form = DetailedPropertyForm(instance=property)
    return render(request, 'add_property_details.html', {'form': form, 'property': property})

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    is_user = property.user == request.user
    return render(request, 'property_detail.html', {'property': property, 'is_user' : is_user})

def save_to_favorites(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        property.is_favorite = True
        property.save()
    return redirect('property_detail', property_id=property_id)

def favorite_properties(request):
    favorite_properties = Property.objects.filter(is_favorite=True)
    return render(request, 'favorite_properties.html', {'favorite_properties': favorite_properties})

def remove_from_favorites(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    property.is_favorite = False
    property.save()
    return redirect('property_detail', property_id=property_id)

def contact(request):
    agent_info = {
        'name': 'Fernanda Escobar',
        'phone': '62380259'
    }
    owner_info = {
        'name': 'Jose Barrientos',
        'phone': '69526417'
    }
    return render(request, 'contact.html', {'agent_info': agent_info, 'owner_info': owner_info})

def perfil(request):
    user_properties = Property.objects.filter(user=request.user)
    return render(request, 'perfil.html', {'user_properties': user_properties})

def custom_logout(request):
    logout(request)
    return redirect('signup')

def report_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user
            incident.save()
            return redirect('home')
    else:
        form = IncidentForm()
    return render(request, 'report_incident.html', {'form': form})


@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = DetailedPropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_detail', property_id=property.id)
    else:
        form = DetailedPropertyForm(instance=property)
    return render(request, 'edit_property.html', {'form': form, 'property': property})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    if property.user != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta propiedad.")
    
    if request.method == "POST":
        property.delete()
        return redirect('home')  # Redirige al perfil del usuario después de eliminar la propiedad

    return render(request, 'delete_property.html', {'property': property})

@login_required
def request_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    fixed_fee_percentage = Decimal('0.01')
    agent_fee_percentage = Decimal('0.025')

    fixed_fee = fixed_fee_percentage * property.price
    agent_fee = agent_fee_percentage * property.price
    total_cost = property.price + fixed_fee + agent_fee

    context = {
        'property': property,
        'fixed_fee': fixed_fee,
        'agent_fee': agent_fee,
        'total_cost': total_cost,
    }
    return render(request, 'request_property.html', context)

@login_required
def process_payment(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    user = request.user

    fixed_fee_percentage = Decimal('0.01')
    agent_fee_percentage = Decimal('0.025')

    fixed_fee = fixed_fee_percentage * property.price
    agent_fee = agent_fee_percentage * property.price
    total_cost = property.price + fixed_fee + agent_fee

    if request.method == 'POST':
        form = BankTransferForm(request.POST)
        if form.is_valid():
            # Simular el proceso de transferencia bancaria
            account_number = form.cleaned_data['account_number']
            bank_name = form.cleaned_data['bank_name']
            swift_code = form.cleaned_data['swift_code']
            amount = form.cleaned_data['amount']

            # Aquí puedes agregar la lógica para manejar el pago real

            # Generar factura
            invoice_id = str(uuid.uuid4())  # Genera un ID único para la factura
            date = datetime.now().strftime('%Y-%m-%d')  # Fecha actual

            invoice_data = {
                'user': user,
                'property': property,
                'invoice_id': invoice_id,
                'date': date,
                'amount': total_cost,
            }

            html = render_to_string('invoice.html', {'invoice': invoice_data})

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'
            pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)
            if pisa_status.err:
                return HttpResponse('Error al generar la factura', status=400)

            return response
    else:
        form = BankTransferForm(initial={'amount': total_cost})

    context = {
        'property': property,
        'form': form,
        'fixed_fee': fixed_fee,
        'agent_fee': agent_fee,
        'total_cost': total_cost,
    }
    return render(request, 'process_payment.html', context)
