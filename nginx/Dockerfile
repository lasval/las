FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY wait-for-it.sh etc/nginx/wait-for-it.sh

# Copy Entrypoint Script
COPY docker-entrypoint.sh etc/nginx/docker-entrypoint.sh
RUN chmod +x etc/nginx/docker-entrypoint.sh