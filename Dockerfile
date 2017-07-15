FROM python:3

# Install su-exec
ADD https://github.com/davesque/su-exec/archive/v0.2.tar.gz /tmp/su-exec
RUN \
  cd /tmp/su-exec/su-exec-0.2 \
  && make \
  && mv su-exec /usr/bin \
  && cd \
  && rm -rf /tmp/su-exec

# Install apt packages
RUN apt-get update

RUN apt-get install -y pdf2svg
RUN apt-get install -y texlive
#RUN apt-get install -y texlive-latex-extra
#RUN apt-get install -y texlive-fonts-extra

# Apt cleanup
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Install pandoc
ARG PANDOC_URL=https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
RUN curl -L -o /pandoc.deb $PANDOC_URL
RUN dpkg -i /pandoc.deb
RUN rm /pandoc.deb

WORKDIR /usr/src/app

COPY requirements ./requirements
COPY requirements.txt ./

# Install pip packages
ARG REQUIREMENTS_FILE=requirements.txt
RUN pip install --no-cache-dir -r $REQUIREMENTS_FILE

COPY . .

# Generate static files
RUN python manage.py compress
RUN python manage.py loadarticles

# Heroku requires that we user a non-root user
RUN useradd -m localuser

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
