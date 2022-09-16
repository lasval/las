FROM nginx:1.19-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost/ || exit 1