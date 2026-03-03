FROM node:current-alpine3.23 AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend .
RUN npm run build

# ---------- Serve ----------
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# React SPA fallback
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]