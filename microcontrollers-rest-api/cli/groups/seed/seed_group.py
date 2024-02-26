from datetime import datetime, timedelta

from cli.groups import BaseGroup
from lib_objects import bcrypt
from database.schemas import User, Acceleration


class SeedGroup(BaseGroup):
    """ Implements methods responsible for seeding database. """
    bcrypt = bcrypt

    def init(self):
        admin = User(username='admin', pw_hash=self.bcrypt.generate_password_hash('admin'))
        acc = Acceleration(timestamp=datetime.now(), x_axis=0, y_axis=0, z_axis=0)

        self.db.session.add(admin)
        self.db.session.add(acc)
        self.db.session.commit()
        print('Database seeded!')

    def users(self):
        user1 = User(username='test1', pw_hash=self.bcrypt.generate_password_hash('test'))
        user2 = User(username='test2', pw_hash=self.bcrypt.generate_password_hash('test'))
        user3 = User(username='test3', pw_hash=self.bcrypt.generate_password_hash('test'))

        self.db.session.add(user1)
        self.db.session.add(user2)
        self.db.session.add(user3)
        self.db.session.commit()
        print('Database seeded!')

    def acc(self):
        acc1 = Acceleration(timestamp=datetime.now() + timedelta(minutes=1), x_axis=1, y_axis=1, z_axis=9.81)
        acc2 = Acceleration(timestamp=datetime.now() + timedelta(hours=1), x_axis=1, y_axis=1, z_axis=9.81)
        acc3 = Acceleration(timestamp=datetime.now() + timedelta(days=1), x_axis=1, y_axis=1, z_axis=9.81)

        self.db.session.add(acc1)
        self.db.session.add(acc2)
        self.db.session.add(acc3)
        self.db.session.commit()
        print('Database seeded!')
