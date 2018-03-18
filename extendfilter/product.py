from mongoengine import *
import extendfilter.searchfilter as sf

connect('mongoengine_test', host='localhost', port=27017)


class Product(Document):
    SearchFilter = sf.SearchFilter
    meta = {'queryset_class': SearchFilter }
    product_id = StringField(required=True, max_length=200)
    name  = StringField(required=True)
    brand = StringField(required=True)
    category = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=50)
    rating = IntField(min_value=1, max_value=5)
    price = FloatField(min_value=100)

# make a post instance that defines a document
product_1 = Product(
    product_id='A1',
    name ='Laptop',
    brand = 'HP',
    category='Electronics',
    description = 'This is HP laptop',
    rating = 4,
    price = 500

)

for post in Product.objects(name__icontains='laptop'):
    print(post.price)



# Product.objects.func_lies_bw(200,700)
# Product.objects.ranges(200, 700)

# if __name__ == "__main__":
