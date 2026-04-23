from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# This starts our Flask app
app = Flask(__name__)

# Secret key for session management - keep this secure!
app.secret_key = b'\xfe\x12\x8e\x15\x13\xbc\xda\x02\x0b\xf4\x12\x8a'

# Database setup: using SQLite for local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# This helps handle foreign key names during migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Hooking up the database and migration tools
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Tools for security and building the API
bcrypt = Bcrypt(app)
api = Api(app)