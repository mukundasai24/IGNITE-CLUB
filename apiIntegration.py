import requests
import logging
from credentialManager import credentials

# Configure basic logging
logging.basicConfig(level=logging.INFO)

class APIIntegration:
    @staticmethod
    def send_to_formsubmit(data):
        """
        Sends registration data securely to FormSubmit from the backend.
        This hides your email and logic from the client side!
        """
        email = credentials.get_formsubmit_email()
        url = f"https://formsubmit.co/ajax/{email}"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Prepare the payload identical to what your frontend used to send
        payload = {
            "_subject": f"✨ New Premium Student Registration: {data.get('name', 'Unknown')}",
            "Full Name": data.get('name', ''),
            "Roll Number": data.get('rollNumber', ''),
            "Department": data.get('department', ''),
            "Interested Domain": data.get('domain', ''),
            "Email Address": data.get('email', ''),
            "Events & Workshops of Interest": data.get('events', '')
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                logging.info(f"Successfully notified FormSubmit for {data.get('name')}")
                return True
            else:
                logging.error(f"FormSubmit API Error: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Failed to connect to FormSubmit API: {str(e)}")
            return False
