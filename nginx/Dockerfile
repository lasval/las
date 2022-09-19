FROM nginx:1.23.1-alpine

RUN apk add vim

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY nginx-green.conf /etc/nginx
COPY nginx-blue.conf /etc/nginx