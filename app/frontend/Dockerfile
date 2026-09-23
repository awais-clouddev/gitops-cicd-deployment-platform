FROM nginx:alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752

RUN apk upgrade --no-cache

COPY nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginx:nginx index.html /usr/share/nginx/html/index.html
COPY --chown=nginx:nginx style.css /usr/share/nginx/html/style.css
COPY --chown=nginx:nginx app.js /usr/share/nginx/html/app.js

USER nginx

EXPOSE 8080

ENTRYPOINT ["nginx", "-g", "daemon off;"]
