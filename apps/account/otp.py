from django.utils.crypto import get_random_string
from threading import Thread
from .models import Otp
import random


# Opt manager class
class OtpManager:
    def __init__(self, mobile=None, token=None):
        if token or mobile:
            # Try to get user_otp object from data or create a new one
            try:
                user_otp = Otp.objects.get(token=token)
            except Otp.DoesNotExist:
                user_otp = Otp.objects.get_or_create(mobile=mobile)[0]

                # Create new random token
                user_otp.token = get_random_string(length=64)
                user_otp.save()

            self.otp = user_otp
        else:
            self.otp = None

    def create_otp(self, request):
        # Create new Rnd Otp and save in sessions
        self.otp.otp = random.randint(10000, 99999)
        self.otp.save()

        request.session["otp_token"] = self.otp.token
        request.session.modified = True

        t1 = Thread(target=self.send_otp)
        t1.start()

    def send_otp(self):
        # Send Otp via SMS
        mobile = self.otp.mobile
        otp = str(self.otp.otp)

        print(otp)

    def delete_otp(self, request):
        # Delete existing otp_token
        if "otp_token" in request.session:
            del request.session["otp_token"]

        try:
            self.otp.delete()
        except Otp.DoesNotExist:
            return None
