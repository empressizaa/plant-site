# Use an ultra-lightweight web server image to host static files
FROM alpine:3.19

# Install a clean web server environment
RUN apk add --no-cache thttpd

# Create a secure hosting directory inside the container virtual drive
WORKDIR /app

# Copy your public site assets straight into the server path
COPY index.html ./

# Open up port 8080 for handling public network traffic
EXPOSE 8080

# Launch the secure background web server on container startup
CMD ["thttpd", "-D", "-h", "0.0.0.0", "-p", "8080", "-d", "/app", "-u", "nobody"]
