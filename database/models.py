import datetime
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

# drop database >>
# mongo
# use note-hub
# db.dropDatabase()
# https://docs.mongodb.com/manual/reference/method/db.dropDatabase/

# mongodb-migrations >> https://github.com/DoubleCiti/mongodb-migrations

class Note(db.Document):
    name = db.StringField(required=True, unique=True)
    content = db.StringField(blank=True, null=True, required=False)

    # https://pymongo.readthedocs.io/en/stable/examples/datetimes.html
    created_at_server_utc_row = db.DateTimeField(default=datetime.datetime.utcnow, required=False)
    created_at_server_local = db.DateTimeField(default=datetime.datetime.now, required=False)
    created_at_client = db.StringField(blank=True, null=True, required=False)

    tags = db.ListField(db.StringField(max_length=100), blank=True, null=True, required=False)
    category = db.StringField(max_length=200, default='')
    active = db.BooleanField(default=True)  # for trash
   # value = db.ListField(IntField(blank=True, null=True), default=lambda: [1, 2, 3])  # for future features
    added_by = db.ReferenceField('User')

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    notes = db.ListField(db.ReferenceField('Note', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Note, 'added_by', db.CASCADE)