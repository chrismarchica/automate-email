#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Check if the required Python packages are installed
python3 -c "import google.oauth2.credentials, google_auth_oauthlib.flow, google.auth.transport.requests, googleapiclient.discovery" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
fi

# Run the Python script
python3 send_email.py 