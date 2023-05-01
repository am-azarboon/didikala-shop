import random
import time


# Create random code and send via SMS
def otp_random_code(mobile=None, request=None):
    random_code = random.randint(10000, 99999)

    request.session['otp_token'] = random_code
    request.modified = True

    time.sleep(8)
    print(random_code)
