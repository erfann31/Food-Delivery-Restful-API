from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from .forms import UserRegistrationForm
from .models import CustomUser


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully. Please check your email for verification.')
            # Send verification email (code to send email here)
            # Assuming your user model generates a verification token during user creation
            user.send_verification_email()  # You'll need to define this method in your model
            return HttpResponse("Email verified successfully sent!")  # You can render a template or redirect as needed    # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})


def delete_user(request):
    CustomUser.objects.all().delete()
    return HttpResponse("Data deleted successfully")


def email_verification_view(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if not user.verified:
            if not user.token_expired():  # Check if the token is not expired
                user.verified = True
                user.save()
                return HttpResponse("Email verified successfully")
            else:
                return HttpResponse("The verification link has expired.")  # Handle expired token
        else:
            return HttpResponse("Email already verified.")
    except CustomUser.DoesNotExist:
        return HttpResponse("Invalid verification token.")
