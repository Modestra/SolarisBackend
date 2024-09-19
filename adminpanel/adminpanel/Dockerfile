FROM node:latest as build
COPY . /usr/src
WORKDIR /usr/src
RUN npm i --force
RUN npm run build

FROM nginx:latest
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /usr/src/dist /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /usr/share/nginx/html/
EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
