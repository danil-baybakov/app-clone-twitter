FROM nginx:latest

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./dist /app/html

COPY ./nginx.conf /etc/nginx/nginx.conf