# Base image selection
# FROM docker.io/python:3.12.3
FROM docker.io/pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

# Install essential utilities
RUN apt-get update && apt-get install -y \
    curl \
    net-tools \
    iputils-ping \
    nano 

# Install Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Install and configure proxychains4 to use Tailscale's SOCKS5 proxy (Optional)
RUN apt-get install -y proxychains4 
RUN sed -i 's/socks4[[:space:]]\+127\.0\.0\.1[[:space:]]\+9050/socks5  127.0.0.1 1055/' /etc/proxychains4.conf

# Upgrade pip and install Python packages
RUN pip install --upgrade pip
RUN pip install flask python-dotenv
RUN pip install jupyterlab ipywidgets

# Configure environment variables to use Tailscale proxy (Optional)
# ENV ALL_PROXY="socks5://localhost:1055/"
# ENV HTTP_PROXY="http://localhost:1055/"
# ENV http_proxy="http://localhost:1055/"

# Set working directory and copy applciation files
WORKDIR /app
COPY hello.py /app
COPY start.sh /app
RUN chmod +x /app/start.sh

# Default startup command
CMD ["./start.sh"]

# the pre-built image: docker.io/saladtechnologies/tailscale:0.0.1-basic-gpu