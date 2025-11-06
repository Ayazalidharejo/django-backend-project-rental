def calculate_deposit(start_date, end_date, daily_rate=50):
    days = (end_date - start_date).days + 1
    total_cost = days * daily_rate
    deposit = total_cost * 0.20
    return round(deposit, 2)


def process_deposit_payment(booking_id, amount, token):
    return {
        'success': True,
        'payment_id': f'mock_payment_{booking_id}',
        'amount': amount,
        'message': 'Deposit payment processed successfully (mock)'
    }


def refund_deposit(booking_id, amount):
    return {
        'success': True,
        'refund_id': f'mock_refund_{booking_id}',
        'amount': amount,
        'message': 'Deposit refund processed successfully (mock)'
    }

