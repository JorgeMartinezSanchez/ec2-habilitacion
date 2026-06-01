FROM nginx:1.27-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/app.conf
COPY nginx/404.html /usr/share/nginx/html/404.html
RUN mkdir /usr/share/nginx/html/frontend
COPY frontend/ /usr/share/nginx/html/frontend
EXPOSE 80
