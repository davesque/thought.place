FROM python:3

# Install apt packages
RUN apt-get update && apt-get install -y --no-install-recommends \
                texlive \
                pdf2svg \
        && rm -rf /var/lib/apt/lists/*

# Install pandoc
RUN curl -L -o /pandoc.deb \
        "https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb"
RUN dpkg -i /pandoc.deb
RUN rm /pandoc.deb

# Heroku requires that we user a non-root user
RUN useradd -m localuser

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements /usr/src/app/requirements
COPY requirements.txt /usr/src/app/

# Install pip packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN chown -R localuser /usr/local /usr/src/app
USER localuser

# Generate static files
RUN python manage.py compress
RUN python manage.py loadarticles

CMD gunicorn thoughtplace.wsgi -b 0.0.0.0:$PORT --log-file -
