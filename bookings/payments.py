"""
Mock Stripe payment integration for deposit handling.
This is a placeholder structure that simulates Stripe payment processing.
"""


class MockStripePayment:
    """
    Mock Stripe payment processor for handling deposit payments.
    
    In a real implementation, this would integrate with Stripe's API
    to process actual payments.
    """
    
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """
        Create a mock payment intent (simulating Stripe's create payment intent).
        
        Args:
            amount: Payment amount in cents
            currency: Currency code (default: 'usd')
            metadata: Additional metadata for the payment
        
        Returns:
            dict: Mock payment intent response
        """
        return {
            'id': f'pi_mock_{amount}_{currency}',
            'object': 'payment_intent',
            'amount': amount,
            'currency': currency,
            'status': 'requires_payment_method',
            'metadata': metadata or {},
            'client_secret': f'pi_mock_{amount}_{currency}_secret',
        }
    
    @staticmethod
    def confirm_payment(payment_intent_id, payment_method='card_mock'):
        """
        Confirm a mock payment (simulating Stripe's confirm payment).
        
        Args:
            payment_intent_id: ID of the payment intent
            payment_method: Payment method identifier
        
        Returns:
            dict: Mock payment confirmation response
        """
        return {
            'id': payment_intent_id,
            'object': 'payment_intent',
            'status': 'succeeded',
            'payment_method': payment_method,
            'charges': {
                'data': [{
                    'id': f'ch_mock_{payment_intent_id}',
                    'amount': 1000,  # Mock amount
                    'status': 'succeeded',
                }]
            }
        }
    
    @staticmethod
    def refund_payment(payment_intent_id, amount=None):
        """
        Create a mock refund (simulating Stripe's refund functionality).
        
        Args:
            payment_intent_id: ID of the payment intent to refund
            amount: Optional refund amount (full refund if None)
        
        Returns:
            dict: Mock refund response
        """
        return {
            'id': f're_mock_{payment_intent_id}',
            'object': 'refund',
            'amount': amount or 1000,
            'currency': 'usd',
            'status': 'succeeded',
            'payment_intent': payment_intent_id,
        }


def process_deposit_payment(booking, amount):
    """
    Process a deposit payment for a booking.
    
    Args:
        booking: Booking instance
        amount: Deposit amount in dollars
    
    Returns:
        dict: Payment processing result
    """
    # Convert to cents for Stripe (mock)
    amount_cents = int(amount * 100)
    
    # Create payment intent
    payment_intent = MockStripePayment.create_payment_intent(
        amount=amount_cents,
        metadata={
            'booking_id': booking.id,
            'user_id': booking.user.id,
            'vehicle_id': booking.vehicle.id,
        }
    )
    
    # In a real implementation, you would:
    # 1. Send payment_intent.client_secret to frontend
    # 2. Frontend uses Stripe.js to collect payment
    # 3. Frontend confirms payment and sends result back
    # 4. Backend verifies payment with Stripe API
    
    # For mock, we'll auto-confirm
    if amount > 0:
        confirmation = MockStripePayment.confirm_payment(payment_intent['id'])
        return {
            'success': True,
            'payment_intent_id': payment_intent['id'],
            'status': confirmation['status'],
            'message': 'Deposit payment processed successfully (mock)'
        }
    
    return {
        'success': False,
        'message': 'Invalid deposit amount'
    }

