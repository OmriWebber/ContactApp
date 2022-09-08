from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'RDS_DB_NAME' in os.environ:
    DATABASE_URL = "postgresql+pg8000://postgres:postgres@database-contact-app.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com/database-contact-app"
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://postgres:postgres@database-contact-app.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com/database-contact-app"
else:
    DATABASE_URL = "sqlite:///database.db"
    application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    


db = SQLAlchemy(application)
engine = create_engine(DATABASE_URL)

@application.route('/')
def hello():
    with engine.connect() as connection:
        query = text("SELECT * FROM chris_greenings_blog")
        blog_posts = connection.execute(query)
        for post in blog_posts:
            print(post["title"])
    return "Hello World!"


@application.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()