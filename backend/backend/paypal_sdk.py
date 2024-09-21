import paypalrestsdk

from .paypal_config import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_API_ENDPOINT, PAYPAL_API_VERSION

paypalrestsdk.configure({
    'mode': 'sandbox',  # or 'live'
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
    'api_endpoint': PAYPAL_API_ENDPOINT,
    'api_version': PAYPAL_API_VERSION,
})