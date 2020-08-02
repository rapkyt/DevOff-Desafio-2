# -------------------------------------
# DOCKERFILE (BASE)
# -------------------------------------
# NOTE: Create a container appropriate for Django and Django-Geo

FROM python:3.6

# NOTE: Update and install system dependencies
#       Django-Geo Libs: binutils, libproj-dev, gdal-bin, libgeoip1, python-gdal
#       Django-i18n Libs: gettext libgettextpo-dev
RUN apt-get update -y && apt-get install -y \
    apt-utils \
    binutils \
    libproj-dev \
    gdal-bin \
    libgeoip1 \
    python3-gdal \
    gettext \
    libgettextpo-dev

# NOTE: Update and install Python dependencies
# TODO: Set poetry version as ENV
RUN pip install -U pip \
    && pip install poetry>=0.12 \
    && poetry config virtualenvs.create false

# NOTE: Copy in a nicer default .bashrc
COPY base/.bashrc /root/
