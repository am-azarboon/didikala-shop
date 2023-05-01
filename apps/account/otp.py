import random
import time


# Create random code and send via SMS
def otp_random_code(value=None):
    random_code = random.randint(10000, 99999)
    time.sleep(5)
    print(random_code)

    return random_code
