from rest_framework_simplejwt.tokens import RefreshToken


class TokenRepository:
    @staticmethod
    def generate_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)