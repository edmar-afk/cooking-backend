from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# ssd
urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    
    path('fooditems/', views.FoodItemListView.as_view(), name='fooditem-list'),
    path('food/<int:id>/', views.FoodItemDetailView.as_view(), name='food-detail'),
    path('recipes/<int:food_id>/', views.RecipeByFoodView.as_view(), name='recipes-by-food'),
    
    
    path('profile/<int:userId>/', views.UserProfileView.as_view(), name='user-profile'),
    
    
    path('favorites/add/', views.AddFavoriteView.as_view(), name='add_favorite'),
    path('favorites/remove/', views.RemoveFavoriteView.as_view(), name='remove_favorite'),
    path('favorites/check/<int:user_id>/<int:food_id>/', views.IsFavoriteView.as_view(), name='is_favorite'),
    path('favorites/<int:user_id>/', views.UserFavoritesView.as_view(), name='get_favorites_by_user'),
    
    
    path('foods/<str:category>/', views.FoodByCategoryView.as_view()),
    
    
    path("upload-food/", views.UploadFoodItemView.as_view()),

]
