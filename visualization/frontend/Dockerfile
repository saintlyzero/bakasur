# Use a lightweight base image
FROM nginx:alpine

# Set the working directory to the NGINX content directory
WORKDIR /usr/share/nginx/html

# Copy the contents of the local 'dist' directory to the container
COPY . .

# Expose port 80 to the outside world
EXPOSE 80
