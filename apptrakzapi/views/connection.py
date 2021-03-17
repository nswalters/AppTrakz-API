from django.conf import settings


class Connection:
    db_path = settings.DATABASES['default']['NAME']
