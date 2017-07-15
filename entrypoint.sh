#!/usr/bin/env bash

exec su-exec \
  localuser \
  gunicorn \
  $SITE_APP_NAME.wsgi \
  -b 0.0.0.0:$PORT \
  --log-file - \
  "$@"
