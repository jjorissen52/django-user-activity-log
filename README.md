This django app intended for writing HTTP log to database and/or watch last user activity.

Features:
- DB router for writing logs to another database.
- Filters for ignoring some queries by URL, HTTP methods and response codes.
- Saving anonymous activity as fake user.
- Autocreation log DB (for postgresql)

# Install:

```
pip install https://github.com/jjorissen52/django-user-activity-log/tarball/master
```

# Quickstart

To your settings file:
```python
#settings.py

INSTALLED_APPS = (
    ...
    'activity_log',
)

# Old middlware style
#MIDDLEWARE_CLASSES = (
#    ...
#    'activity_log.middleware.ActivityLogMiddleware',
#)

MIDDLEWARE = (
    ...
    'activity_log.middleware.ActivityLogMiddleware',
)

DATABASE_APPS_MAPPING = {'activity_log': 'logs'}
```

migrate
```
python manage.py migrate
```

If you intend to use a separate database for logging, you should also
add something to the effect of:
```
#settings.py
DATABASE_ROUTERS = ['activity_log.router.DatabaseAppsRouter']
DATABASES = {
    . . .
    'logs': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'logs',
            'USER': config.get(DB_REGION, 'db_user'),
            'PASSWORD': config.get(DB_REGION, 'db_password'),
            'HOST': os.environ['PG'],
            'HOST': 'localhost',
            'PORT': config.get(DB_REGION, 'db_port'),
        },
    }
```

If you are using `psycopg2` as a database backend, you can run:
```
python manage.py create_logging_database
python manage.py migrate --database=logs
```

# Available Settings/Defaults:
- `ACTIVITYLOG_AUTOCREATE_DB = False` Create DB automatically (for postgres, and may be mysql).
    - Note: Does not seem to create the logging database automatically. Run `python manage.py create_logging_database` if the setting does not work.
- `ACTIVITYLOG_ANONIMOUS = True` log anonymous actions
- `ACTIVITYLOG_LAST_ACTIVITY = True` Update last activity datetime in user profile. Needs updates for user model. (See below)
- `ACTIVITYLOG_METHODS = ('POST', 'GET')` Specify HTTP methods to be logged.
- `ACTIVITYLOG_STATUSES = (200, )` List of response statuses which are logged. By default - all logged.
    - Don't use with `ACTIVITYLOG_EXCLUDE_STATUSES`
- `ACTIVITYLOG_EXCLUDE_STATUSES = (302, )` List of response statuses which are ignore.
    - Don't use with `ACTIVITYLOG_STATUSES`
- `ACTIVITYLOG_EXCLUDE_URLS = ('/admin/activity_log/activitylog', )` URL substrings which are ignored.


# Track `LAST_ACTIVITY`

```python
from django.contrib.auth.models import AbstractUser
from activity_log.models import UserMixin

# Only for LAST_ACTIVITY = True
class User(AbstractUser, UserMixin):
    pass
```

Don't forget to migrate!
```
python manage.py migrate & python manage.py migrate --database=logs
```

If you use `ACTIVITYLOG_AUTOCREATE_DB` migrations to logs database 
will be run automatically.
