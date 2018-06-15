from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from activity_log.exceptions import ImproperylConfigured

DATABASE_APPS_MAPPING = getattr(settings, 'DATABASE_APPS_MAPPING', None)
if DATABASE_APPS_MAPPING is not None:
    LOGGING_DATABASE = DATABASE_APPS_MAPPING.get('activity_log', None)
else:
    LOGGING_DATABASE = None


class Command(BaseCommand):
    help = 'Deletes the initial Postgres database'

    def handle(self, *args, **options):
        if not LOGGING_DATABASE:
            raise ImproperylConfigured('DATABASE_APPS_MAPPING must be specified in accordance with the documentation.')

        DATABASE = settings.DATABASES.get(LOGGING_DATABASE, None)
        if DATABASE is None:
            raise ImproperylConfigured(f'DATABASES must be configured to include the database referenced in '
                                       f'DATABASE_APPS_MAPPING. Your logging database should be named' + LOGGING_DATABASE)

        self.stdout.write(self.style.SUCCESS('Starting DB creation..'))

        engine = DATABASE.get('ENGINE', '')
        if 'postgresql' not in engine and 'psycopg' not in engine:
            raise ImproperylConfigured('logging database must be postgres.')

        dbname = DATABASE['NAME']
        user = DATABASE.get('USER', 'postgres')
        password = DATABASE.get('PASSWORD', 'postgres')
        host = DATABASE.get('HOST', 'localhost')
        port = DATABASE.get('PORT', '5432')

        self.stdout.write(self.style.SUCCESS('Connecting to host..'))
        con = connect(dbname='postgres', user=user, host=host, password=password, port=port)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.stdout.write(self.style.SUCCESS('Dropping database'))
        cur = con.cursor()
        try:
            cur.execute('DROP DATABASE ' + dbname)
        except Exception as e:
            print(e)
        cur.close()

        con.close()

        self.stdout.write(self.style.SUCCESS('All done!'))