#!/usr/bin/env python
"""
Standalone M-Pesa test script to debug API connectivity
Run this script to test your M-Pesa credentials without Django
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

import requests
import base64
import json
from datetime import datetime
from decouple import config

def test_mpesa_credentials():
    """Test M-Pesa API credentials and connectivity"""
    
    print("🔍 M-Pesa Credentials Test")
    print("=" * 40)
    
    # Load credentials
    try:
        consumer_key = config('DARAJA_CONSUMER_KEY')
        consumer_secret = config('DARAJA_CONSUMER_SECRET')
        shortcode = config('DARAJA_SHORTCODE')
        passkey = config('DARAJA_PASSKEY')
        environment = config('DARAJA_ENVIRONMENT', 'sandbox')
        
        print(f"✅ Environment: {environment}")
        print(f"✅ Shortcode: {shortcode}")
        print(f"✅ Consumer Key: {consumer_key[:10]}...")
        print(f"✅ Consumer Secret: {consumer_secret[:10]}...")
        print(f"✅ Passkey: {passkey[:10]}...")
        
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return False
    
    # Set base URL
    if environment == 'sandbox':
        base_url = 'https://sandbox.safaricom.co.ke'
    else:
        base_url = 'https://api.safaricom.co.ke'
    
    print(f"🌐 Base URL: {base_url}")
    
    # Test 1: Get Access Token
    print("\n🔑 Testing Access Token Generation...")
    try:
        url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        # Create auth string
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f"Basic {auth_base64}"
        }
        
        print(f"📡 Making request to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                access_token = data['access_token']
                print(f"✅ Access token obtained: {access_token[:20]}...")
                print(f"⏰ Expires in: {data.get('expires_in', 'Unknown')} seconds")
                
                # Test 2: STK Push
                print("\n📱 Testing STK Push...")
                return test_stk_push(base_url, access_token, shortcode, passkey)
            else:
                print(f"❌ No access token in response: {data}")
                return False
        else:
            print(f"❌ Failed to get access token: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your internet connection.")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your internet connection.")
        return False
    except Exception as e:
        print(f"❌ Error getting access token: {e}")
        return False

def test_stk_push(base_url, access_token, shortcode, passkey):
    """Test STK Push functionality"""
    
    try:
        # Generate password
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{shortcode}{passkey}{timestamp}"
        password_bytes = password_str.encode('ascii')
        password = base64.b64encode(password_bytes).decode('ascii')
        
        # STK Push URL
        url = f"{base_url}/mpesa/stkpush/v1/processrequest"
        
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        
        # Test phone number (sandbox)
        test_phone = "254708374149"
        
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,  # Test with 1 KSH
            "PartyA": test_phone,
            "PartyB": shortcode,
            "PhoneNumber": test_phone,
            "CallBackURL": "https://mydomain.com/path",  # Dummy callback for testing
            "AccountReference": "TechPulse-Test",
            "TransactionDesc": "Test Transaction"
        }
        
        print(f"📡 Making STK Push request to: {url}")
        print(f"📱 Test phone number: {test_phone}")
        print(f"💰 Amount: 1 KSH")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📋 Response: {json.dumps(data, indent=2)}")
            
            if data.get('ResponseCode') == '0':
                print("✅ STK Push initiated successfully!")
                print(f"🆔 CheckoutRequestID: {data.get('CheckoutRequestID')}")
                print(f"💬 Customer Message: {data.get('CustomerMessage')}")
                return True
            else:
                print(f"❌ STK Push failed: {data.get('ResponseDescription', 'Unknown error')}")
                return False
        else:
            print(f"❌ STK Push request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in STK Push: {e}")
        return False

def test_network_connectivity():
    """Test basic network connectivity"""
    
    print("\n🌐 Testing Network Connectivity...")
    
    test_urls = [
        "https://google.com",
        "https://sandbox.safaricom.co.ke",
        "https://api.safaricom.co.ke"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {e}")

if __name__ == "__main__":
    print("🚀 M-Pesa Integration Test Suite")
    print("=" * 50)
    
    # Test network connectivity first
    test_network_connectivity()
    
    # Test M-Pesa credentials
    success = test_mpesa_credentials()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! M-Pesa integration is working.")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Go to subscription page")
        print("3. Use test phone number: 254708374149")
        print("4. Note: In sandbox mode, no real STK push will appear on phones")
    else:
        print("❌ Tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Verify your credentials in Safaricom Developer Portal")
        print("2. Check your internet connection")
        print("3. Ensure you're using the correct environment (sandbox/production)")
        print("4. Try regenerating your API credentials")
