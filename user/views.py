from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from food.models import Food
from restaurant.models import Restaurant
from .forms import UserRegistrationForm
from .models import CustomUser
from .serializers import CustomUserSerializer


def delete_user(request):
    CustomUser.objects.all().delete()
    return HttpResponse("Data deleted successfully")


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
def add_to_favorites(request):
    user_id = request.data.get('user_id')
    restaurant_ids = request.data.get('restaurant_ids', [])
    food_ids = request.data.get('food_ids', [])

    try:
        user = CustomUser.objects.get(pk=user_id)

        # Add specified restaurants to user's favorites
        for restaurant_id in restaurant_ids:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            user.favorite_restaurants.add(restaurant)

        # Add specified foods to user's favorites
        for food_id in food_ids:
            food = Food.objects.get(pk=food_id)
            user.favorite_foods.add(food)

        return Response({'message': 'Added to favorites successfully'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Restaurant.DoesNotExist:
        return Response({'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
    except Food.DoesNotExist:
        return Response({'message': 'Food not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_profile(request, user_id):
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


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
