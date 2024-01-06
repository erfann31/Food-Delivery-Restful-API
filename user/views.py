from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from food.models.food import Food
from food.serializers.food_serializer import FoodSerializer
from restaurant.models.restaurant import Restaurant
from restaurant.serializers import RestaurantSerializer
from user.forms.forms import UserRegistrationForm
from .models import CustomUser
from .serializers import CustomUserSerializer


class TokenObtainPairView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Generate token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token})
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.send_verification_email()
            serialized_user = CustomUserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def email_verification_view(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if not user.verified:
            if not user.verification_token_expired():
                user.verified = True
                user.save()
                return HttpResponse("Email verified successfully")
            else:
                return HttpResponse("The verification link has expired.")
        else:
            return HttpResponse("Email already verified.")
    except CustomUser.DoesNotExist:
        return HttpResponse("Invalid verification token.")


@api_view(['POST'])
def password_reset_request(request):
    if request.method == 'POST':
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.generate_password_reset_token()
            user.send_password_reset_email()
            return Response({'message': "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def password_reset_confirm(request, token):
    user = CustomUser.objects.filter(password_reset_token=token).first()
    if not user or user.password_reset_token_expired():
        return HttpResponse("Invalid or expired token.")

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.password_reset_token = ''
        user.save()
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
        return Response({'error': 'At least one restaurant_id or food_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUser.objects.get(pk=user.id)
        for restaurant_id in restaurant_ids:
            try:
                restaurant = Restaurant.objects.get(pk=restaurant_id)
                user.favorite_restaurants.add(restaurant)
            except Restaurant.DoesNotExist:
                return Response({'message': f'Restaurant with ID {restaurant_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        for food_id in food_ids:
            try:
                food = Food.objects.get(pk=food_id)
                user.favorite_foods.add(food)
            except Food.DoesNotExist:
                return Response({'message': f'Food with ID {food_id} not found'}, status=status.HTTP_404_NOT_FOUND)

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
        return Response({'error': 'At least one restaurant_id or food_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(pk=user.id)

        for restaurant_id in restaurant_ids:
            try:
                restaurant = Restaurant.objects.get(pk=restaurant_id)
                user.favorite_restaurants.remove(restaurant)
            except Restaurant.DoesNotExist:
                return Response({'message': f'Restaurant with ID {restaurant_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        for food_id in food_ids:
            try:
                food = Food.objects.get(pk=food_id)
                user.favorite_foods.remove(food)
            except Food.DoesNotExist:
                return Response({'message': f'Food with ID {food_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Removed from favorites successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user_id = request.user.id

    try:
        user = CustomUser.objects.get(pk=user_id)
        updated_data = {}
        if 'name' in request.data:
            updated_data['name'] = request.data['name']
        if 'mobile_number' in request.data:
            updated_data['mobile_number'] = request.data['mobile_number']
        if 'photo' in request.data:
            updated_data['photo'] = request.data['photo']

        serializer = CustomUserSerializer(instance=user, data=updated_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_favorites(request):
    user = request.user

    try:
        custom_user = CustomUser.objects.get(pk=user.id)
        favorite_restaurants = custom_user.favorite_restaurants.all()
        favorite_foods = custom_user.favorite_foods.all()

        restaurant_serializer = RestaurantSerializer(favorite_restaurants, many=True)
        food_serializer = FoodSerializer(favorite_foods, many=True)

        return Response({
            'favorite_restaurants': restaurant_serializer.data,
            'favorite_foods': food_serializer.data
        }, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
