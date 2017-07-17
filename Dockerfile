FROM python:3

# Install latex packages
RUN apt-get update \
  && apt-get install -y \
    pdf2svg \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install pandoc
ARG PANDOC_URL=https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
RUN \
  curl -L -o /tmp/pandoc.deb $PANDOC_URL \
  && dpkg -i /tmp/pandoc.deb \
  && rm /tmp/pandoc.deb

WORKDIR /usr/src/app

COPY requirements ./requirements
COPY requirements.txt ./

# Install pip packages
ARG REQUIREMENTS_FILE=requirements.txt
RUN pip install --no-cache-dir -r $REQUIREMENTS_FILE

COPY . .

# Collect/generate static files
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
