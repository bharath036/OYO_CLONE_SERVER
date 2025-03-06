from django.contrib.auth.backends import ModelBackend
from .models import Hotelvendor

class VendorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            vendor = Hotelvendor.objects.get(username=username)
            if vendor.check_password(password):  # Ensure password is checked correctly
                return vendor
        except Hotelvendor.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Hotelvendor.objects.get(pk=user_id)
        except Hotelvendor.DoesNotExist:
            return None
