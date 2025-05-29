#!/bin/bash

echo "🔍 Complete M-Pesa Debug & Fix Script"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Please run this script from your Django project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install missing dependencies
echo "📦 Installing missing dependencies..."
pip install requests==2.31.0 python-decouple==3.8

# Install all requirements
echo "📦 Installing all requirements..."
pip install -r requirements.txt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Check .env file
echo "📋 Checking .env file..."
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your M-Pesa credentials"
    exit 1
fi

# Check required environment variables
echo "📋 Checking M-Pesa credentials..."
CONSUMER_KEY=$(grep DARAJA_CONSUMER_KEY .env | cut -d'=' -f2)
CONSUMER_SECRET=$(grep DARAJA_CONSUMER_SECRET .env | cut -d'=' -f2)
SHORTCODE=$(grep DARAJA_SHORTCODE .env | cut -d'=' -f2)
PASSKEY=$(grep DARAJA_PASSKEY .env | cut -d'=' -f2)

if [ -z "$CONSUMER_KEY" ] || [ -z "$CONSUMER_SECRET" ] || [ -z "$SHORTCODE" ] || [ -z "$PASSKEY" ]; then
    echo "❌ Missing M-Pesa credentials in .env file!"
    echo "Required variables: DARAJA_CONSUMER_KEY, DARAJA_CONSUMER_SECRET, DARAJA_SHORTCODE, DARAJA_PASSKEY"
    exit 1
fi

echo "✅ All credentials found"

# Test network connectivity
echo "🌐 Testing network connectivity..."
curl -s --connect-timeout 5 https://google.com > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Internet connection OK"
else
    echo "❌ No internet connection"
    exit 1
fi

# Test Safaricom API connectivity
echo "🌐 Testing Safaricom API connectivity..."
curl -s --connect-timeout 10 https://sandbox.safaricom.co.ke > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Safaricom API reachable"
else
    echo "❌ Cannot reach Safaricom API"
fi

# Run Django checks
echo "🔧 Running Django system checks..."
python manage.py check

if [ $? -eq 0 ]; then
    echo "✅ Django checks passed"
else
    echo "❌ Django checks failed"
    exit 1
fi

# Run M-Pesa test
echo "📱 Running M-Pesa integration test..."
python blog/mpesa_test.py

echo ""
echo "🚀 Debug complete!"
echo ""
echo "If everything looks good, you can now:"
echo "1. Run: python manage.py runserver"
echo "2. Go to: http://127.0.0.1:8000/accounts/register/"
echo "3. Register and login"
echo "4. Go to: http://127.0.0.1:8000/blog/subscribe/"
echo "5. Test with phone number: 254708374149"
echo ""
echo "📝 Important notes:"
echo "- In sandbox mode, use test phone numbers only"
echo "- Real phones won't receive STK push in sandbox"
echo "- Check logs/mpesa.log for detailed logs"
echo "- Use 'python manage.py test_mpesa' for quick testing"
