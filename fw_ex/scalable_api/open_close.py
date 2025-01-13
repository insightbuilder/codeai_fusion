class PaymentProcessor:
    def process_payment(self):
        raise NotImplementedError


class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self):
        print("Processing credit card payment...")


class PayPalPaymentProcessor(PaymentProcessor):
    def process_payment(self):
        print("Processing PayPal payment...")


payment_methods = [CreditCardPaymentProcessor(), PayPalPaymentProcessor()]

for method in payment_methods:
    method.process_payment()
