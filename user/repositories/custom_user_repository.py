from user.models import CustomUser


class CustomUserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        return CustomUser.objects.get(pk=user_id)

    @staticmethod
    def update_user_profile(user, updated_data):
        for key, value in updated_data.items():
            setattr(user, key, value)
        user.save()

    @staticmethod
    def get_user_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_verification_token(token):
        try:
            return CustomUser.objects.get(verification_token=token)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_reset_password_token(token):
        try:
            return CustomUser.objects.get(password_reset_token=token)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def generate_password_reset_token(user):
        user.generate_password_reset_token()
        user.save()

    @staticmethod
    def reset_password(user, new_password):
        user.set_password(new_password)
        user.password_reset_token = ''
        user.save()

    @staticmethod
    def update_user_verification_status(user):
        user.verified = True
        user.save()

    @staticmethod
    def check_verification_token_expired(user):
        return user.verification_token_expired()

    @staticmethod
    def check_password_reset_token_expired(user):
        return user.password_reset_token_expired()
