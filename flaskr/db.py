import sqlite3

import click

from flask import current_app  #proxy to current_app
from flask import g  # global object to store data in current app context
from flask.cli import with_appcontext


# g provides ability to store connection to database and reuse it
# on next call instead of creating new connection.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        return g.db

# creates tables from sql file
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db') # binds function to CLI command
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initializing database')

# register database functions with Flask app (called by factory)
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

