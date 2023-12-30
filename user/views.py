from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from .forms import UserRegistrationForm
from .models import CustomUser


def delete_user(request):
    CustomUser.objects.all().delete()
    return HttpResponse("Data deleted successfully")


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully. Please check your email for verification.')
            user.send_verification_email()
            return HttpResponse("Email verified successfully sent!")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})


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


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.generate_password_reset_token()
            user.send_password_reset_email()
            return HttpResponse("Password reset link sent to your email.")
        else:
            return HttpResponse("User not found.")
    return render(request, 'password_reset_request.html')


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
