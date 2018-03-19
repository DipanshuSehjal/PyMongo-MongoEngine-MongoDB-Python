from mongoengine import *

'''
This class acts as an API for a cart functionality of a e-commerce website
'''


# QuerySet is used to subclass queries set manager for mongoengine
class Cart():

    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.inventory = {}
        self.total_items = 0
        self.total_price = 0

    def add_to_cart(self, kwargs):
        '''

        :param kwargs: dict of item with price and qty
        e.g. { Item_id: [Item_name, Price, qty] }
        :return:
        '''
        self.inventory.update(kwargs)
        # get the only value in list: qty
        self.total_items += int([qty[2] for qty in kwargs.values()].pop())
        # get the total price: price*qty
        price = list(kwargs.values())
        # print(price)
        self.total_price += price[0][1] * price[0][2]

    def view_cart(self):
        for item, value in self.inventory.items():
            print('Item: ' + value[0] +
                  '\n    Item Id: ' + item +
                  '\n    Price: ' + str(value[1]) +
                  '\n    Qty: ' + str(value[2]))
            print('====')

        print('Total price: ' + str(self.total_price))
        print('Total items: ' + str(self.total_items))

    def checkout_cart(self):
        ''' Connect to DB '''
        connect('mongoengine_cart', host='localhost', port=27017)
        for item, value in self.inventory.items():
            prod = CartStructure(
                cart_id = self.cart_id,
                item_id = item,
                item_name = value[0],
                price = value[1],
                quantity = value[2]
            )            
            prod.save()


    def _update_total_price(self, price, delete=False):
        ''' if delete then reduce the total price of the cart
        Here, del_price is the price to be reduced
        '''
        if delete:
            self.total_price -= price
        else:
            self.total_price += price

    def _update_total_items(self, qty, delete=False):
        '''
        if delete then reduce the total qty of the cart
        Here, del_qty is the quantity to be reduced
        :return:
        '''
        if delete:
            self.total_items -= qty
        else:
            self.total_items += qty


    def delete_item(self, item_id):
        del_item = self.inventory.pop(item_id, None)

        # update the total items and price
        if del_item:
            ''' Update the total amount of cart and items in the cart'''
            self._update_total_price(delete=True, price=del_item[1]*del_item[2])
            self._update_total_items(delete=True, qty=del_item[2])


    def change_qty(self, item_id, qty):
        '''
            {item_id: [item_name, price, qty]}
        :param item_id:
        :param qty:
        :return:
        '''
        if qty < 1:
            raise ValueError('qty can not be less than 1')
        else:
            temp =  self.inventory[item_id]
            # increase in qty. temp[2] is quantity

            if temp[2] < qty:
                change = qty-temp[2]
                temp[2] = qty
                print(temp)
                self.inventory.update({item_id:temp})
                print(self.inventory)
                # update the total items and price
                self._update_total_items(qty=change)
                self._update_total_price(price=temp[1]*(change))
            elif temp[2] > qty: # decrease in qty
                change = temp[2]-qty
                temp[2] = qty
                self.inventory.update({item_id: temp})
                # update the total items and price
                self._update_total_items(qty= -change)
                self._update_total_price(price= -(temp[1]*(change)))


class CartStructure(Document):
    ''' This is for the external queryset_class

        cart id:
            item_id, item_name, price, qty

    '''
    # meta = {'queryset_class': SearchFilter }
    cart_id = StringField(required=True, max_length=200)
    item_id = StringField(required=True)
    item_name = StringField(required=True)  # done
    price = FloatField(required=True)  #
    quantity = IntField(required=True)


my_cart = Cart("Dipa1")
# {item: [price, qty]}
my_cart.add_to_cart({'A1': ['Laptop', 550, 2]})
my_cart.add_to_cart({'A2': ['T-shirt',150, 2]})
my_cart.add_to_cart({'A3': ['Mobile', 400, 2]})
my_cart.add_to_cart({'A4': ['Watch', 1000, 2]})


my_cart.view_cart()
# load the cart to MongoDB
my_cart.checkout_cart()


# delete the item
# delete an item not in the list
my_cart.delete_item('A4')

my_cart.change_qty('A2', 1)