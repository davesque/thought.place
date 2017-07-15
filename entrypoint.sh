#!/usr/bin/env bash

exec \
  gunicorn "$SITE_APP_NAME.wsgi" \
  --bind "0.0.0.0:$PORT" \
  --log-file - \
  "$@"
