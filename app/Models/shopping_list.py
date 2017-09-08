import uuid

class Shoppinglist(object):
    def __init__(self, name, id = None):
        self.name = name
        self.id = uuid.uuid4().hex if id is None else id
        # self.created_time = created_time
        # self.user_id = user_id
        # self.activities = {}
    