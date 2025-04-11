#!/bin/bash

# Start the Tailscale daemon with userspace networking mode in the backgound and continue running other commands
echo -e "\nJoining the Tailscale network..."
tailscaled --tun=userspace-networking --socks5-server=localhost:1055 --outbound-http-proxy-listen=localhost:1055 &
sleep 5

# Disable DNS resolution through Tailscale (customize as needed)
tailscale set --accept-dns=false

# Bring up Tailscale using the provided auth key and machine ID or 'LOCAL' as fallback
tailscale up --auth-key=$TAILSCALE_AUTH_KEY --hostname ${SALAD_MACHINE_ID:-LOCAL}
sleep 5

# Enable Tailscale SSH on this device
tailscale set --ssh

# Retrieve and export the local Tailscale IP, making it accessible for local applications
echo -e "\nRetrieve the Tailscale IP..."
export TAILSCALE_IP=$(tailscale ip | head -n 1)
echo -e "\nTailscale IP for this device: $TAILSCALE_IP"

# Capture and store all environment variables, includeing system and user environment variables
# Optionally, you can filter specific variables to be saved 
printenv > /etc/environment

# Run the application 1 on port 8888 with dual-stack support (IPv4 and IPv6)
echo -e "\nRunning the Python code on port 8888..."
python hello.py &

# Run the application 2 on port 8889 with dual-stack support (IPv4 and IPv6)
echo -e "\nRunning Jupyter Lab on port 8889 ..."
jupyter lab --no-browser --port=8889  --ip=* --allow-root  --NotebookApp.token='' &

# Keeping the script running indefinitely
echo -e "\nSleeping indefinitely..."
sleep infinity

# The containers running on SaladCloud must have a continuously running process;
# and if the process completes, SaladCloud will automatically reallocate the instances to rerun the image.