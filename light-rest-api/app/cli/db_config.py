from app import app, db


@app.cli.command('db_create')
def db_create():
    """ Creates all database tables. """
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    """ Drops all database tables. """
    db.drop_all()
    print('Database dropped!')
