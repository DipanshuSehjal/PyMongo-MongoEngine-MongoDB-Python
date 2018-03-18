from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)


class SearchFilter(QuerySet):

    def __init__(self):
        pass

    def ranges(self, minvalue, maxvalue, include=True):
        '''    :param minvalue: min value default (included)
               :param maxvalue: max value default (included)
               :return: list of result

               '''
        if not isinstance(minvalue, int) and not isinstance(maxvalue, int):
            raise ValueError("minvalue and maxvalue has to be integers")

        if minvalue > maxvalue:
            raise ValueError("Min value should be less than max value")

        list_1 = []
        if include == True:
            for prod_1 in Product.objects(price__gte=minvalue):
                list_1.append(prod_1)
        else:
            for prod_1 in Product.objects(price__gt=minvalue):
                list_1.append(prod_1)

        # 2. look for the less than
        list_2 = []
        if include == True:
            for prod_2 in Product.objects(price__lte=maxvalue):
                list_2.append(prod_2)
        else:
            for prod_2 in Product.objects(price__lt=maxvalue):
                list_2.append(prod_2)

        # final list
        res_list = []
        for res in list_2:
            if res in list_1:
                res_list.append(res)
        print('Printing from the function')
        for res in res_list:
            print(res.price)
        print('End printing from the function')
        return res_list


    def search_name(self, name, exact=False, caseinsensitive=True, startswith=False, endswith=False,
                    contains=True):
        '''BY default the name contains the keyword'''

        if exact:
            if caseinsensitive: # case insensitive
                return Product.objects(name__iexact=name)
            else: # not case insensitive
                return Product.objects(name__exact=name)

        if startswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(name__istartswith=name)
            else:  # not case insensitive
                return Product.objects(name__startswith=name)

        if endswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(name__iendswith=name)
            else:  # not case insensitive
                return Product.objects(name__endswith=name)

        if contains:
            if caseinsensitive:  # case insensitive
                return Product.objects(name__icontains=name)
            else:  # not case insensitive
                return Product.objects(name__contains=name)


    def search_price(self, value, lt=False, gt=False, include=True, ne=False, range=False,
                     minvalue=0, maxvalue=0):
        ''' lt has the precedence. If lt and gt is true then function will return lt values'''

        if lt:
            if include:
                return Product.objects(price__lte=value)
            else:
                return Product.objects(price__lt=value)

        if gt:
            if include:
                return Product.objects(price__gte=value)
            else:
                return Product.objects(price__gt=value)

        if ne:
            return Product.objects(price__ne=value)

        ''' Use range to use the 'lies between' functionality of a search capability.
        minvalue and maxvalue are necessary  
        '''
        if range:
            return SearchFilter.ranges(self, minvalue=minvalue, maxvalue=maxvalue, include=include)


    def search_brand(self, brandname, exact=False, caseinsensitive=True, startswith=False,
                     endswith=False, contains=True):
        if exact:
            if caseinsensitive: # case insensitive
                return Product.objects(brand__iexact=brandname)
            else: # not case insensitive
                return Product.objects(brand__exact=brandname)

        if startswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(brand__istartswith=brandname)
            else:  # not case insensitive
                return Product.objects(brand__startswith=brandname)

        if endswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(brand__iendswith=brandname)
            else:  # not case insensitive
                return Product.objects(brand__endswith=brandname)

        if contains:
            if caseinsensitive:  # case insensitive
                return Product.objects(brand__icontains=brandname)
            else:  # not case insensitive
                return Product.objects(brand__contains=brandname)


    def search_category(self, categoryname, exact=False, caseinsensitive=True, startswith=False,
                        endswith=False, contains=True):
        if exact:
            if caseinsensitive: # case insensitive
                return Product.objects(category__iexact=categoryname)
            else: # not case insensitive
                return Product.objects(category__exact=categoryname)

        if startswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(category__istartswith=categoryname)
            else:  # not case insensitive
                return Product.objects(category__startswith=categoryname)

        if endswith:
            if caseinsensitive:  # case insensitive
                return Product.objects(category__iendswith=categoryname)
            else:  # not case insensitive
                return Product.objects(category__endswith=categoryname)

        if contains:
            if caseinsensitive:  # case insensitive
                return Product.objects(category__icontains=categoryname)
            else:  # not case insensitive
                return Product.objects(category__contains=categoryname)




sf = SearchFilter()
for prod in sf.search_category(categoryname='electr',  startswith=True):
    print(prod.category)

for prod in sf.search_price(range=True, minvalue=150, maxvalue=600, value=0):
    print(prod.price)

for prod in sf.search_price(value=150, gt=True):
    print(prod.price)



class Product(Document):
    SearchFilter = SearchFilter
    meta = {'queryset_class': SearchFilter }
    product_id = StringField(required=True, max_length=200)
    name  = StringField(required=True) # done
    brand = StringField(required=True) #
    category = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=50)
    rating = IntField(min_value=1, max_value=5)
    price = FloatField(min_value=100)

for post in Product.objects(name__icontains='laptop'):
    print(post.price)