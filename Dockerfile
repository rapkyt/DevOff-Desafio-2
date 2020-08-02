# -------------------------------------
# DOCKERFILE
# -------------------------------------
# Notes:
#   * You must build sama_web/web before building this image!
#   * This Dockerfile _must be at the project root_ to be compatible with Heroku Container CLI
#
# See:
#   * Dockerfile Best Practices: https://goo.gl/ZQh6da

FROM devoff/web

# Build Args
# =====================================
# These are passed via the --build-arg flag during `docker build`
ARG WORKERS

# ENV Setup
# =====================================

# Single line form is preferred for caching
ENV PYTHONPATH=/usr/app/project:/usr/app/project/vendor \
    DJANGO_SETTINGS_MODULE=app.config.settings.prod \
    WORKERS=$WORKERS

# Working Dir Setup
# =====================================
# We're about to work with the local context alot,
# let's make paths a little easir

WORKDIR /usr/app

# Install Dependencies
# =====================================a

COPY poetry.lock /usr/app
COPY pyproject.toml /usr/app

# TODO: Need a way to run this with --no-dev for production
# SEE: https://stackoverflow.com/a/54763270/1082663
RUN poetry install --no-interaction --no-ansi --no-dev

# NOTE: Mostly everything that follows will invalidate the cache

# Copy Local Files
# =====================================
# NOTE: COPY <src> ... <dest> dirs without leading slashes are relative to WORKDIR

COPY .webenv .env
COPY django/manage.py manage.py
COPY django/project/app project/app
COPY django/project/static project/static

# Run Collect Static
# =====================================

RUN python manage.py collectstatic --no-input

# Cleanup
# =====================================

RUN rm -rf \
/usr/app/poetry.lock \
/usr/app/pyproject.toml \
/usr/app/.env \
/usr/app/project/static

# User Setup
# =====================================
# Recommended best-practice, run the image as non-root

RUN groupadd -r heroku && useradd --no-log-init -r -g heroku heroku
USER heroku

# Start the App
# =====================================
# CMD is required to run on Heroku
# $PORT is set by Heroku

CMD gunicorn app.config.wsgi --bind 0.0.0.0:$PORT -w $WORKERS -k gevent
