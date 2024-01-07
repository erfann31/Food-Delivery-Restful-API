from rest_framework_simplejwt.tokens import RefreshToken

from user.utils.token_expiration_utils import verification_token_expired, password_reset_token_expired
from user.utils.token_generator import generate_password_reset_token


class TokenRepository:
    @staticmethod
    def generate_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


    @staticmethod
    def generate_password_reset_token(user):
        user.password_reset_token = generate_password_reset_token(user)
        user.save()

    @staticmethod
    def check_verification_token_expired(user):
        return verification_token_expired(user.verification_token)

    @staticmethod
    def check_password_reset_token_expired(user):
        return password_reset_token_expired(user.password_reset_token_created_at)
