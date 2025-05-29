import base64
import json
import logging
import requests
from datetime import datetime
from decouple import config

# Set up logging
logger = logging.getLogger(__name__)

class MpesaClient:
    """
    M-Pesa API Client for handling STK Push and other M-Pesa transactions
    """
    
    def __init__(self):
        self.env = config('DARAJA_ENVIRONMENT', 'sandbox')
        self.consumer_key = config('DARAJA_CONSUMER_KEY')
        self.consumer_secret = config('DARAJA_CONSUMER_SECRET')
        self.shortcode = config('DARAJA_SHORTCODE')
        self.passkey = config('DARAJA_PASSKEY')
        self.callback_url = config('DARAJA_CALLBACK_URL')
        
        # Set the base URL based on environment
        if self.env == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
        
        # Log initialization
        logger.info(f"MpesaClient initialized in {self.env} environment")
    
    def get_access_token(self):
        """Get OAuth access token from Safaricom"""
        try:
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            
            # Create auth string and encode to base64
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f"Basic {auth_base64}"
            }
            
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            if 'access_token' in response_data:
                logger.info("Access token obtained successfully")
                return response_data['access_token']
            else:
                logger.error(f"Failed to get access token: {response_data}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting access token: {str(e)}")
            return None
    
    def generate_password(self):
        """Generate the M-Pesa API password using the provided shortcode and passkey"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.shortcode}{self.passkey}{timestamp}"
        password_bytes = password_str.encode('ascii')
        return base64.b64encode(password_bytes).decode('ascii'), timestamp
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiate an STK push request
        
        Args:
            phone_number (str): Customer phone number (format: 254XXXXXXXXX)
            amount (int): Amount to be charged
            account_reference (str): Reference ID for the transaction
            transaction_desc (str): Description of the transaction
            
        Returns:
            dict: Response from M-Pesa API
        """
        try:
            # Get access token
            access_token = self.get_access_token()
            if not access_token:
                return {"error": "Could not get access token"}
            
            # Generate password and timestamp
            password, timestamp = self.generate_password()
            
            # Prepare STK push request
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            
            headers = {
                'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json'
            }
            
            # Clean and validate phone number
            phone_number = str(phone_number).strip()
            if not phone_number.startswith('254'):
                logger.warning(f"Phone number {phone_number} doesn't start with 254, might cause issues")
            
            # Log the request details (excluding sensitive info)
            logger.info(f"Initiating STK push for {phone_number} with amount {amount}")
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": self.callback_url,
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            # Make the request
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            
            # Log the response
            if 'ResponseCode' in response_data and response_data['ResponseCode'] == '0':
                logger.info(f"STK push initiated successfully: {response_data['CheckoutRequestID']}")
            else:
                logger.error(f"STK push failed: {response_data}")
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error in STK push: {str(e)}")
            return {"error": str(e)}
    
    def check_transaction_status(self, checkout_request_id):
        """
        Check the status of an STK push transaction
        
        Args:
            checkout_request_id (str): The CheckoutRequestID from the STK push response
            
        Returns:
            dict: Response from M-Pesa API
        """
        try:
            # Get access token
            access_token = self.get_access_token()
            if not access_token:
                return {"error": "Could not get access token"}
            
            # Generate password and timestamp
            password, timestamp = self.generate_password()
            
            # Prepare status request
            url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
            
            headers = {
                'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            # Make the request
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
            
        except Exception as e:
            logger.error(f"Error checking transaction status: {str(e)}")
            return {"error": str(e)}
