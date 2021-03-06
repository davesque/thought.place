FROM python:3.6-slim-stretch

# Install pandoc
ARG PANDOC_URL=https://github.com/jgm/pandoc/releases/download/2.0.5/pandoc-2.0.5-1-amd64.deb
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && curl -L -o /tmp/pandoc.deb $PANDOC_URL \
    && dpkg -i /tmp/pandoc.deb \
    && rm /tmp/pandoc.deb \
    && apt-get purge --auto-remove -y \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y \
    pdf2svg \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements ./requirements
COPY requirements.txt ./

# Install pip packages
ARG REQUIREMENTS_FILE=requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && pip install --no-cache-dir -r $REQUIREMENTS_FILE \
    && apt-get purge --auto-remove -y \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python manage.py collectstatic
RUN python manage.py compress
RUN python manage.py loadarticles

# Heroku containers are not run with root privileges.  We add and enforce a
# non-root user here to ensure that our site works under these conditions.  The
# actual runtime user chosen by Heroku will vary.  See here:
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
RUN useradd -m localuser
USER localuser

CMD ["/usr/src/app/entrypoint.sh"]
