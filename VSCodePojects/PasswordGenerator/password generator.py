import string
import random

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Specify the desired length of the password
password_length = 12

# Generate a random password of the specified length
generated_password = generate_password(password_length)

print(f"Generated Password: {generated_password}")
