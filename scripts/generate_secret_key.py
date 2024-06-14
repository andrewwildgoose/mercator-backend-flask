import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_secret_key():
    # Generate 24 random bytes
    secret_key_bytes = os.urandom(24)
    
    # Convert to a hexadecimal string
    secret_key = secret_key_bytes.hex()
    
    return secret_key

def write_secret_key_to_env(secret_key):
    with open('../.env', 'a') as f:
        f.write(f"\nSECRET_KEY='{secret_key}'\n")

if __name__ == '__main__':
    new_secret_key = generate_secret_key()
    write_secret_key_to_env(new_secret_key)
    print("SECRET_KEY generated and saved to .env file.")
