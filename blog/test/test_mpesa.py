from django.core.management.base import BaseCommand
from blog.mpesa import MpesaClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test M-Pesa integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            default='254708374149',
            help='Phone number to test with (default: 254708374149)'
        )
        parser.add_argument(
            '--amount',
            type=int,
            default=1,
            help='Amount to test with (default: 1)'
        )

    def handle(self, *args, **options):
        phone_number = options['phone']
        amount = options['amount']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing M-Pesa with phone: {phone_number}, amount: {amount}')
        )
        
        try:
            # Initialize M-Pesa client
            mpesa_client = MpesaClient()
            
            # Test access token
            self.stdout.write('Getting access token...')
            token = mpesa_client.get_access_token()
            
            if token:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Access token obtained: {token[:20]}...')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to get access token')
                )
                return
            
            # Test STK push
            self.stdout.write('Initiating STK push...')
            response = mpesa_client.stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference='TechPulse-Test',
                transaction_desc='Test Transaction'
            )
            
            if 'ResponseCode' in response and response['ResponseCode'] == '0':
                self.stdout.write(
                    self.style.SUCCESS(f'✅ STK push successful: {response["CheckoutRequestID"]}')
                )
                self.stdout.write(f'Customer Message: {response["CustomerMessage"]}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ STK push failed: {response}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
