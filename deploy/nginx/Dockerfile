FROM nginx

COPY ./deploy/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./deploy/nginx/conf.d /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]
