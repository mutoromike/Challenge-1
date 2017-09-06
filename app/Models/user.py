import uuid

class User(object):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        #self.id = uuid.uuid4().hex if id is None else id



        