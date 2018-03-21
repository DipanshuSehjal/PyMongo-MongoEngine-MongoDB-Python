'''Note to self. To make a new collection, first close the previous collection.
Otherwise the documents will be with the class name'''

from mongoengine import *

class UserStructure(Document):
    user_id = StringField(required=True)
    password = StringField(required=True)
    name = StringField(required=True)
    email_id = StringField(required=True)
    phone = StringField(required=True)


class UserAccount:

    # add/search a user to mongoDB,
    def __init__(self, user_id, password, name, email_id, phone):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.email_id = email_id
        self.phone = phone

    def add_user(self):
        # connect to the DB
        connect('mongoengine_user_account', host='localhost', port=27017)
        '''Note to self. To make a new collection, first close the previous collection.
        Otherwise the documents will be with the class name'''

        user = UserStructure(
            user_id = self.user_id,
            password = self.hash_password(),
            name = self.name,
            email_id = self.email_id,
            phone = self.phone
        ).save()

    def hash_password(self):
        from passlib.hash import pbkdf2_sha256
        '''The encrypt() function takes three parameters. The first parameter is the password to be hashed. 
        The second parameter is much more interesting. It controls the number of iterations that PBKDF2 applies to the password. 
        By tuning this parameter, PBKDF2 can be configured to require large amounts of computing time to complete. 
        A common question about using PBKDF2 is about the number of rounds to use. Unfortunately, there is no one magic number. 
        Instead, developers should benchmark the time required for a certain iteration count on the system they are deploying the code 
        on and tune it until it’s acceptable. The higher the iteration count the better of course. 
        The third setting is the length of the salt in bytes that Passlib generates for you. 
        The default of 16 bytes if the parameter isn’t specified is fine.'''
        hash = pbkdf2_sha256.encrypt(self.password, rounds=200000, salt_size=16)
        return hash

    '''retrieve password = pbkdf2_sha256.verify("password", hash)'''


# user_id, password, name, email_id, phone
user = UserAccount(user_id='Dip123', password="password",
                   name='Dipanshu', email_id='dip@gmail.com', phone='123')

user.add_user()
