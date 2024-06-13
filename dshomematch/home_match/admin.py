from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from home_match.models import CustomUser
from .models import ErrorLog, Incident, Property

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Property)
admin.site.register(Incident)
admin.site.register(ErrorLog)

