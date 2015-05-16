from flask.ext.script import Manager, prompt, prompt_bool, prompt_pass

from harpy_network import app, db
from harpy_network.models.users import User
manager = Manager(app)

@manager.command
def createdb():
    """
    Creates the database tables.
    """
    db.create_all()
    print("Database created.")

@manager.command
def destroydb():
    """
    Destroys the database tables.
    """
    if prompt_bool("Are you sure you wish to destroy your database tables? This is not reversible."):
        db.drop_all()
        print("Database destroyed.")

@manager.command
def create_user(email=None, password=None, admin=None):
    """
    Creates a new user.
    """
    if email is None:
        email = prompt("email")
    if password is None:
        password = prompt_pass("password")
    if admin is None:
        admin = prompt_bool("Make this user an admin?")
    new_user = User(email, password, admin)
    db.session.add(new_user)
    db.session.commit()
    print("New User Created.")

if __name__ == "__main__":
    manager.run()