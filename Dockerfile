FROM python:3

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
RUN curl -L -o /tmp/pandoc.deb $PANDOC_URL
RUN dpkg -i /tmp/pandoc.deb
RUN rm /tmp/pandoc.deb

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

# Heroku requires that we use a non-root user
RUN useradd -m localuser
USER localuser

CMD ["/usr/src/app/entrypoint.sh"]
