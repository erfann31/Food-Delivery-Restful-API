from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from food.serializers.food_serializer import FoodSerializer
from restaurant.serializers.restaurant_serializer import RestaurantSerializer
from user.forms.forms import UserRegistrationForm
from user.serializers.custom_user_serializer import CustomUserSerializer
from .models import CustomUser
from .repositories.custom_user_repository import CustomUserRepository
from .repositories.token_repository import TokenRepository
from .repositories.user_favorite_repository import UserFavoriteRepository
from .utils.email_sender import send_verification_email, send_password_reset_email


class TokenObtainPairView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            access_token = TokenRepository.generate_token_for_user(user)
            return Response({'access_token': access_token})
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_user(request):
    form = UserRegistrationForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        send_verification_email(user)
        user.save()
        serialized_user = CustomUserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def email_verification_view(request, token):
    user = CustomUserRepository.get_user_by_verification_token(token)
    if user:
        if not user.verified:
            if not TokenRepository.check_verification_token_expired(user):
                CustomUserRepository.update_user_verification_status(user)
                return HttpResponse("Email verified successfully")
            else:
                return HttpResponse("The verification link has expired.")
        else:
            return HttpResponse("Email already verified.")
    return HttpResponse("Invalid verification token.")


@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    user = CustomUserRepository.get_user_by_email(email)
    if user:
        TokenRepository.generate_password_reset_token(user)
        send_password_reset_email(user)
        return Response({'message': "Password reset link sent to your email."}, status=status.HTTP_200_OK)
    else:
        return Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)


def password_reset_confirm(request, token):
    user = CustomUserRepository.get_user_by_reset_password_token(token)
    if not user or TokenRepository.check_password_reset_token_expired(user):
        return HttpResponse("Invalid or expired token.")
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        CustomUserRepository.reset_password(user, new_password)
        return HttpResponse("Password reset successfully.")
    return render(request, 'password_reset_confirm.html')


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    user = request.user
    if 'restaurant_ids' not in request.data or 'food_ids' not in request.data:
        return Response({'error': 'Both restaurant_ids and food_ids are required and must be a list!'}, status=status.HTTP_400_BAD_REQUEST)

    restaurant_ids = request.data.get('restaurant_ids', [])
    food_ids = request.data.get('food_ids', [])
    if not restaurant_ids and not food_ids:
        return Response({'error': 'At least one restaurant_ids or food_ids field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        for restaurant_id in restaurant_ids:
            UserFavoriteRepository.add_favorite_restaurant(user.id, restaurant_id)

        for food_id in food_ids:
            UserFavoriteRepository.add_favorite_food(user.id, food_id)

        return Response({'message': 'Added to favorites successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_favorites(request):
    user = request.user
    restaurant_ids = request.data.get('restaurant_ids', [])
    food_ids = request.data.get('food_ids', [])

    if not restaurant_ids and not food_ids:
        return Response({'error': 'At least one restaurant_ids or food_ids field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        for restaurant_id in restaurant_ids:
            UserFavoriteRepository.remove_favorite_restaurant(user.id, restaurant_id)

        for food_id in food_ids:
            UserFavoriteRepository.remove_favorite_food(user.id, food_id)

        return Response({'message': 'Removed from favorites successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user_id = request.user.id
    try:
        user = CustomUserRepository.get_user_by_id(user_id)
        updated_data = {}
        if 'name' in request.data:
            updated_data['name'] = request.data['name']
        if 'mobile_number' in request.data:
            updated_data['mobile_number'] = request.data['mobile_number']
        if 'photo' in request.data:
            updated_data['photo'] = request.data['photo']

        if user:
            CustomUserRepository.update_user_profile(user, updated_data)
            return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_favorites(request):
    user = request.user

    try:
        favorite_restaurants, favorite_foods = UserFavoriteRepository.get_user_favorites(user.id)

        if favorite_restaurants is not None and favorite_foods is not None:
            restaurant_serializer = RestaurantSerializer(favorite_restaurants, many=True)
            food_serializer = FoodSerializer(favorite_foods, many=True)

            return Response({
                'favorite_restaurants': restaurant_serializer.data,
                'favorite_foods': food_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
