from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #Funiona (1)
    path('custom_login/', views.custom_login, name='custom_login'), #Funciona(2)
    path('signup/', views.signup, name='signup'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),#Nueva
    path('property/<int:property_id>/save_to_favorites/', views.save_to_favorites, name='save_to_favorites'),
    path('favorite_properties/', views.favorite_properties, name='favorite_properties'),
    path('property/<int:property_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('contact/', views.contact, name='contact'),
    path('perfil/', views.perfil, name='perfil'), 
    path('logout/', views.custom_logout, name='custom_logout'),
    path('signup/logout/', views.custom_logout, name='custom_logout'),
    ]


