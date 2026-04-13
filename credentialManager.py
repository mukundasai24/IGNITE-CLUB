import os
from dotenv import load_dotenv

class CredentialManager:
    def __init__(self):
        # Load environment variables from a .env file if it exists
        load_dotenv()
    
    @staticmethod
    def get_formsubmit_email():
        # Retrieves email from environment securely, with fallback
        return os.environ.get("FORMSUBMIT_EMAIL", "mukundeswarasai2007@gmail.com")
    
    @staticmethod
    def get_secret_key():
        # Example of how you would secure session keys or JWT secrets
        return os.environ.get("SECRET_KEY", "super-secret-dev-key")

# Create a singleton instance for easy imports across your backend
credentials = CredentialManager()
