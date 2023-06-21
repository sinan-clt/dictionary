from django.urls import path
from app.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register', Register.as_view(), name='register_user'),
    path('login', UserLogin.as_view(), name='login_user'),
    path('user_details', authenticatedUserDetails.as_view(), name='user_details'),

    path('list_word/', ListwordsAPI.as_view(), name='list_word'),
    path('create_word/', CreateAPI.as_view(), name='create_word'),
    path('detail_word/<int:word_id>', DetailAPI.as_view(), name='word_detail'),
    path('update_word/<int:word_id>', UpdateAPI.as_view(), name='word_update'),
    path('delete_word/<int:word_id>', DeleteAPI.as_view(), name='word_delete'),
    path('search_word/', SearchWordAPI.as_view(), name='search_word'),


]

