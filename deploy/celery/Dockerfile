FROM global_touch/base:latest

RUN celery -A periodic worker --loglevel=info -E -Q QUEUE_RECOMMENDATIONS
RUN celery -A periodic worker --loglevel=info -E -Q QUEUE_EMAILS
RUN celery -A periodic worker --loglevel=info -E -Q QUEUE_OVERFLOWED_CONNECTIONS