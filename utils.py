import re
import sqlite3

from contextlib import closing
from flask import Flask
from unidecode import unidecode


def establish_db_connection(db):
    """
    Establish a connection to the database passed by the calling function.
    """
    return sqlite3.connect(db)

def initialize_db():
    """
    Before the application can be run, the database must be constructed. Using
    the sqlite3 <path> < <schemafile> command requires that the host have
    sqlitee3 installed, which isn't always the case.

    initialize_db() makes life easier by allowing the developer to initialize
    the database in three simple steps:

    1) $ python
    2) >>> from utils import initialize_db
    3) >>> initialize_db()
    """
    logr = Flask(__name__)
    logr.config.from_object('config')

    try:
        with closing(establish_db_connection(logr.config['DATABASE_FILE'])) as db:
            with logr.open_resource('schema.sql') as f:
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
