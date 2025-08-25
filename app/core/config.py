import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@localhost:3306/fastapi_db")
ADMIN_DATABASE_URL = os.getenv("ADMIN_DATABASE_URL", "mysql+mysqlconnector://root:root@localhost:3306/admin_db")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-256-bit-secret-key-here-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Print configuration for debugging
print(f"Main Database URL: {DATABASE_URL}")
print(f"Admin Database URL: {ADMIN_DATABASE_URL}")
print(f"Secret Key: {SECRET_KEY[:20]}...")
print(f"Algorithm: {ALGORITHM}")
print(f"Token Expire Minutes: {ACCESS_TOKEN_EXPIRE_MINUTES}")






