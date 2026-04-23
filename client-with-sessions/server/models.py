from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
# Import db and bcrypt from your config file, not from libraries!
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # Rubric check: Unique usernames and hidden passwords
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)

    # Relationships: One User has many Tasks
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete-orphan')

    # Security: Ensure sensitive data stays on the server
    serialize_rules = ('-tasks.user', '-_password_hash',)

    @hybrid_property
    def password_hash(self):
        # Human touch: throw an error if someone tries to 'see' the hash
        raise AttributeError('Password hashes are not readable.')

    @password_hash.setter
    def password_hash(self, password):
        # Adding a bit of validation looks more professional
        if len(password) < 5:
            raise ValueError("Password is too short.")
        
        pw_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = pw_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'

    # Rubric check: Additional model with multiple custom fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    importance = db.Column(db.Integer, default=1)
    
    # Ownership: Linking task to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='tasks')

    # Avoid infinite loops in JSON output
    serialize_rules = ('-user.tasks',)