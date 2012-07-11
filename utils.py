import re
import sqlite3

from contextlib import closing
from flask import Flask
from unidecode import unidecode


"""
Establish a connection to the database passed by the calling function. 
"""
def establish_db_connection(db):
    return sqlite3.connect(db)


"""
Before the application can be run, the database must be constructed. However,
using the sqlite3 <path> < <schemafile> command requires that the host have
sqlite3 installed, which isn't always the case.

We make life easier by allowing the developer to follow these simple steps:

1) $ python
2) >>> from utils import initialize_db
3) >>> initialize_db()
"""
def initialize_db():

    application = Flask(__name__)
    application.config.from_object('config')

    try:
        with closing(establish_db_connection(application.config['DATABASE'])) as db:
            with application.open_resource('schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()
        print "Database successfully initialized!"
    except Error as e:
        print "Error({0}): {1}".format(e.errno, e.strerror)


def slugify(text):
    """
    Generates an ASCII-only slug.
    """
    return re.sub('-$', '', re.sub('[^A-Za-z0-9\-]+', '-', text))
