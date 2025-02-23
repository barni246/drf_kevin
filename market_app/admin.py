from django.contrib import admin

# Register your models here.
from .models import Market, Seller, Product  # Importiere deine Modelle

# Modelle im Django Admin registrieren
admin.site.register(Market)
admin.site.register(Seller)
admin.site.register(Product)