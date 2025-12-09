from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import FoodItem, Recipe, Profile, Favorites
from .serializers import FoodItemSerializer, RecipeSerializer, ProfileSerializer, FavoriteSerializer, FoodItemCreateWithRecipeSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodItemListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer


class FoodItemDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    lookup_field = 'id'
    
class RecipeByFoodView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer

    def get_queryset(self):
        food_id = self.kwargs.get('food_id')
        return Recipe.objects.filter(food_item__id=food_id)
    
    
class UserProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, userId):
        user = get_object_or_404(User, id=userId)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AddFavoriteView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_id = request.data.get('user_id')
        food_id = request.data.get('food_id')

        if not user_id or not food_id:
            return Response({'error': 'Missing user_id or food_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            food_item = FoodItem.objects.get(id=food_id)
        except (User.DoesNotExist, FoodItem.DoesNotExist):
            return Response({'error': 'User or FoodItem not found'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorites.objects.get_or_create(user=user, food_item=food_item)

        if not created:
            return Response({'message': 'Already favorited'}, status=status.HTTP_200_OK)

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveFavoriteView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_id = request.data.get('user_id')
        food_id = request.data.get('food_id')

        try:
            favorite = Favorites.objects.get(user__id=user_id, food_item__id=food_id)
            favorite.delete()
            return Response({'message': 'Removed from favorites'}, status=status.HTTP_200_OK)
        except Favorites.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)

class IsFavoriteView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id, food_id):
        is_favorited = Favorites.objects.filter(user__id=user_id, food_item__id=food_id).exists()
        return Response({'is_favorited': is_favorited}, status=status.HTTP_200_OK)

class UserFavoritesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        favorites = Favorites.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    
class FoodByCategoryView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return FoodItem.objects.filter(category__iexact=category)
    


class UploadFoodItemView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()
