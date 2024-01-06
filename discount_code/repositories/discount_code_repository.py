from discount_code.models.discount_code import DiscountCode


class DiscountCodeRepository:
    @staticmethod
    def get_discount_code_by_text(code_text):
        try:
            return DiscountCode.objects.get(code_text=code_text, is_active=True)
        except DiscountCode.DoesNotExist:
            return None