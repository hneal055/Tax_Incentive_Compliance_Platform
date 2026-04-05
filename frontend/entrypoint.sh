#!/bin/sh
# Substitute $PORT in nginx config at runtime.
# Railway injects PORT; local Docker defaults to 3000.
PORT=${PORT:-3000}
sed -i "s/listen 3000;/listen ${PORT};/g" /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
