from __future__ import absolute_import
from celery import Celery
from celery.signals import task_failure

import settings
import rollbar

# Error Tracking

rollbar.init("52839cbb5d2b478ca55d8766ce6b47f1", settings.ENV_NAME)


def celery_base_data_hook(request, data):
    data['framework'] = 'celery'


rollbar.BASE_DATA_HOOK = celery_base_data_hook

# Define the app initialization

app = Celery("periodic", broker=settings.RABBIT_URL, include=["match.tasks"])

# Define schedule

app.conf.beat_schedule = {
    f"{settings.TASK_RECOMMENDATION_FIND_CONNECTION}-every-1-minute": {
        "task": settings.TASK_RECOMMENDATION_FIND_CONNECTION,
        "schedule": settings.SCHEDULE_RECOMMENDATION_FIND_CONNECTION,
        "options": {"queue": settings.QUEUE_RECOMMENDATIONS}
    },
    f"{settings.TASK_ALERT_CONNECTION}-every-1-minute": {
        "task": settings.TASK_ALERT_CONNECTION,
        "schedule": settings.SCHEDULE_TASK_ALERT_CONNECTION,
        "options": {"queue": settings.QUEUE_EMAILS}
    },
}

app.conf.timezone = "UTC"


# Hooks

@task_failure.connect
def handle_task_failure(**kw):
    rollbar.report_exc_info(extra_data=kw)
