# Use an official NGINX image
FROM nginx:alpine

# Copy static files to NGINX's HTML directory
COPY index.html /etc/nginx/html/

# Copy Nginx reverse proxy config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]