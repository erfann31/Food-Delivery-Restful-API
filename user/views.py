from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password'],
    ),
    responses={
        200: openapi.Response(description='Successful authentication', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'access_token': openapi.Schema(type=openapi.TYPE_STRING)})),
        401: openapi.Response(description='Invalid credentials', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)})),
    },
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def token_obtain_pair_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        access_token = TokenRepository.generate_token_for_user(user)
        return Response({'access_token': access_token})
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'password', 'name']
    ),
    responses={201: 'Created', 400: 'Bad Request', 500: 'Internal Server Error'},
)
@api_view(['POST'])
def register_user(request):
    form = UserRegistrationForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        if send_verification_email(user):
            user.save()
            serialized_user = CustomUserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to send verification email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email']
    ),
    responses={200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'},
)
@api_view(['POST'])
def resend_verification_email(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user.verified:
        return Response({'error': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

    if send_verification_email(user):
        return Response({'message': 'Verification email sent successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to send verification email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'restaurant_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'food_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        },
        required=['restaurant_ids', 'food_ids'],
    ),
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            format="Bearer <token>",
        ),
    ],
    responses={
        200: openapi.Response(description='Added to favorites successfully', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)})),
        400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
        404: openapi.Response(description='User not found', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)})),
    },
)
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
