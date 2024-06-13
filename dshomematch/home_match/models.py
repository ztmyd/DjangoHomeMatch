from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

class Property(models.Model):
    SALE_OR_RENT_CHOICES = [
        ('sale', 'Venta'),
        ('rent', 'Alquiler'),
    ]
    
    ZONE_CHOICES = [
        ('central', 'Zona Céntrica'),
        ('south', 'Zona Sur'),
        ('north', 'Zona Norte'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('house', 'Casa'),
        ('apartment', 'Departamento'),
    ]

    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('rented', 'Alquilado'),
        ('sold', 'Vendido'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sale_or_rent = models.CharField(max_length=4, choices=SALE_OR_RENT_CHOICES)
    zone = models.CharField(max_length=10, choices=ZONE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    is_favorite = models.BooleanField(default=False)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    number_of_bathrooms = models.IntegerField(blank=True, null=True)
    number_of_parking_spaces = models.IntegerField(blank=True, null=True)
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    number_of_elevators = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    accepts_pets = models.BooleanField(default=False)
    social_area = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    image1 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image7 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image8 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES) 

    def __str__(self):
        return f"{self.title} - {self.get_sale_or_rent_display()} - {self.price}"

class Incident(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('In Progress', 'In Progress'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    responsible_team = models.CharField(max_length=255)
    current_status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Incident {self.id} - {self.description[:50]}"

class ErrorLog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Error 404 at {self.path} ({self.timestamp})"