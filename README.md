# The Harpy Network
A Flask based website for tracking prestation (boons) for your favourite Vampire Mind's Eye Theatre LARP.

To start the development server:

```
python manage.py runserver
```

To create the database:

```
python manage.py createdb
```

Alternatively, for database migration support use Alembic:

Create an alembic.ini file in the root directory of the project. (See alembic.ini.sample for an example). Point the
alembic.ini driver to your desired database, then type the following command.

```
alembic upgrade head
```

Deployment Instructions:

* Make a config.py configuration file. See the config.py.sample for an example configuration.
* Initialize your preferred database, either through the createdb script in manage.py or through alembic.
* You may be required to install additional packages depending on your choice of database (e.g. MYSQL-python).

NOTE: This project is a work in progress. The data model will change significantly as the project evolves. To keep up
 with database migrations, I recommend you use alembic. Alembic migration scripts will be included in the repository.