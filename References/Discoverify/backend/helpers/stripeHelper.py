# import os
# import stripe   #3rd party module to handle payments and other functionalities with APIs

# stripe.api_key = os.getenv('STRIPE_API_KEY')

# class StripeHelper:
#     @staticmethod
#     def cancel_stripe_subscription(stripe_id):
#         return stripe.Subscription.delete(stripe_id)