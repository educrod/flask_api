# Dockerfile

# FROM directive instructing base image to build upon

FROM nginx:latest
RUN touch /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/nginx/conf.d/nginx.conf /etc/nginx/conf.d
