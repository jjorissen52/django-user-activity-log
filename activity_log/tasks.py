from . import conf
from . models import ActivityLog
import importlib

if conf.CELERY_APP_MODULE:
    app = getattr(importlib.import_module(conf.CELERY_APP_MODULE, 'celery'), conf.CELERY_APP_NAME)

    @app.task(bind=True)
    def log_activity(self, user_id, user, request_url, request_method, response_code, ip_address, extra_data):
        ActivityLog.objects.create(
            user_id=user_id,
            user=user,
            request_url=request_url,
            request_method=request_method,
            response_code=response_code,
            ip_address=ip_address,
            extra_data=extra_data
        )