from flask.ext.script import Manager

from harpy_network import app, db

manager = Manager(app)

@manager.command
def createdb():
    """
    Creates the database tables.
    """
    db.create_all()

if __name__ == "__main__":
    manager.run()