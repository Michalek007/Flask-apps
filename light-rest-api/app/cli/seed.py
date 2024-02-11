from datetime import datetime

from app import app, bcrypt, db
from database.schemas import User, Performance


@app.cli.command('db_seed_users')
def db_seed_users():
    """ Seeds users table with tests data. """
    user1 = User(username='test1', pw_hash=bcrypt.generate_password_hash('test'))
    user2 = User(username='test2', pw_hash=bcrypt.generate_password_hash('test'))
    user3 = User(username='test3', pw_hash=bcrypt.generate_password_hash('test'))

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    print('Database seeded!')


@app.cli.command('db_seed_params')
def db_seed_params():
    """ Seeds performance table with tests data. """
    param1 = Performance(timestamp=datetime.now(), memory_usage=50, cpu_usage=20, disk_usage=50)
    param2 = Performance(timestamp=datetime.now(), memory_usage=50, cpu_usage=20, disk_usage=50)
    param3 = Performance(timestamp=datetime.now(), memory_usage=50, cpu_usage=20, disk_usage=50)

    db.session.add(param1)
    db.session.add(param2)
    db.session.add(param3)
    db.session.commit()
    print('Database seeded!')


@app.cli.command('db_init')
def db_init():
    """ Initialises database table with necessary data. """
    admin = User(username='admin', pw_hash=bcrypt.generate_password_hash('admin'))

    db.session.add(admin)
    db.session.commit()
    print('Database seeded!')
