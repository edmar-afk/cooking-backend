from django.contrib import admin
from .models import Profile, FoodItem, Recipe, Favorites

admin.site.register(Profile)
admin.site.register(FoodItem)
admin.site.register(Recipe)
admin.site.register(Favorites)
