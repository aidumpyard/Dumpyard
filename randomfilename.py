import random
import string

# Generate a random string of 10 characters
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

print(random_string)