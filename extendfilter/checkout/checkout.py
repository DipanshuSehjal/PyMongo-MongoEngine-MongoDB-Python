from mongoengine import *

class Customer(Document):
    customer_id = StringField(required=True),
    cust_name = StringField(required=True),
    cust_email = StringField(required=True)

class CheckoutStructure(Document):

    customer_id = StringField(required=True)
    cart_id = StringField(required=True)
    transaction_id = StringField(required=True)
    card_number = StringField(required=True)
    payment_mode = StringField(required=True)
    amount = FloatField(required=True)
    success = StringField(required=True)


class Checkout():

    def __init__(self, customer_id, cart_id, card_number, cvv, payment_mode, amount):
        self.customer_id = customer_id
        self.cart_id = cart_id
        self.card_number = card_number
        self.cvv = cvv
        self.payment_mode = payment_mode
        self.amount = amount

    def checkout(self):

        try:
            self._validate_card_number(self.card_number)
        except:
            raise Exception("invalid card number")

        try:
            self._validate_cvv(self.cvv)
        except:
            raise Exception("invalid cvv")

        trans_id = self._generate_transaction_id()

        checkout_object = CheckoutStructure(
            customer_id = self.customer_id,
            cart_id = self.cart_id,
            transaction_id = trans_id,
            card_number = self.card_number,
            payment_mode = self.payment_mode,
            amount = self.amount,
            success = "Yes"
        )

        '''   checkout_object = CheckoutStructure(
            customer_id='12',
            cart_id='12',
            transaction_id='12',
            card_number='12',
            payment_mode='4',
            amount=12,
            success="Yes"
        )
        '''
        self._save_record(checkout_object)

    def _validate_card_number(self, card_number):
        pass

    def _validate_cvv(self, cvv):
        pass

    def _generate_transaction_id(self):
        return 'trans123456789'

    def _save_record(self, obj):
        connect('mongoengine_checkout', host='localhost', port=27017)
        obj.save()

#  customer_id, cart_id, card_number,cvv, payment_mode, amount)
checkout = Checkout(customer_id='Dipanshu1', cart_id='Dipa1', card_number='1234567887654321',cvv='789', payment_mode='Credit', amount=500.99)


checkout.checkout()