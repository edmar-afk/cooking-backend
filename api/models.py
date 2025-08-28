from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

class FoodItem(models.Model):
    name = models.TextField()
    title = models.TextField()
    description = models.TextField()
    serve = models.TextField()
    image = models.ImageField(
        upload_to='food_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    

    def __str__(self):
        return self.name

class Recipe(models.Model):
    food_item = models.ForeignKey(FoodItem, related_name='recipes', on_delete=models.CASCADE)
    recipes = models.TextField()
    instruction = models.TextField()

    audio1 = models.FileField(
        upload_to='food_audio1/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])]
        
    )
    audio2 = models.FileField(
        upload_to='food_audio2/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])]
        
    )
    def __str__(self):
        return f"{self.food_item.name}"


class Favorites(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, related_name='favorited_by', on_delete=models.CASCADE)
    fav_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} favorited {self.food_item.name}"
