# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, FoodItem, Recipe, Favorites

class RegisterSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        profile_picture = validated_data.pop('profile_picture', None)
        validated_data['email'] = validated_data['username']  # map username = email
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, bio=bio, profile_picture=profile_picture)
        return user
    
    
    
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        
        
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_picture']
        

class FavoriteSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'food_item', 'fav_added']


class FoodItemCreateWithRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(required=False)

    class Meta:
        model = FoodItem
        fields = ['name', 'title', 'description', 'serve', 'image', 'category', 'recipe']

    def run_validation(self, data=serializers.empty):
        mutable = data.copy()
        recipe_data = {
            "recipes": data.get("recipe[recipes]"),
            "instruction": data.get("recipe[instruction]"),
        }
        mutable["recipe"] = recipe_data
        return super().run_validation(mutable)

    def create(self, validated_data):
        recipe_data = validated_data.pop("recipe", None)
        food = FoodItem.objects.create(**validated_data)
        if recipe_data:
            Recipe.objects.create(food_item=food, **recipe_data)
        return food

