FROM python:3.8-alpine

ARG ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/usr/src/app:${PYTHONPATH}"
ENV DJANGO_SETTINGS_MODULE="visitors_book.settings.${ENVIRONMENT}"

WORKDIR /usr/src/app
COPY setup.py ./
RUN if [ "$ENVIRONMENT" = development ]; then pip install -e .[devel]; fi
RUN if [ "$ENVIRONMENT" = production ]; then pip install .; fi

ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
