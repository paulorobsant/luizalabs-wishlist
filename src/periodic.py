from __future__ import absolute_import

from celery import Celery
# from celery.schedules import crontab

import settings

# Define the app initialization

app = Celery("periodic", broker=settings.RABBIT_URL, include=["match.tasks"])

# Define schedule

app.conf.beat_schedule = {
    f"{settings.TASK_RECOMMENDATION_FIND_CONNECTION}-every-1-minute": {
        "task": settings.TASK_RECOMMENDATION_FIND_CONNECTION,
        "schedule": 10.0,
        "options": {"queue": settings.QUEUE_RECOMMENDATIONS}
    },
    # f"{settings.TASK_RECOMMENDATION_FIND_CONNECTION_FOR_OVERFLOWED}-every-2-minutes": {
    #     "task": settings.TASK_RECOMMENDATION_FIND_CONNECTION,
    #     "schedule": crontab(minute=2)
    # }
}

app.conf.timezone = "UTC"
app.control.add_consumer(settings.QUEUE_RECOMMENDATIONS, reply=True)