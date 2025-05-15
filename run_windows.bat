@echo off

REM Check if the required Python packages are installed
python -c "import google.oauth2.credentials, google_auth_oauthlib.flow, google.auth.transport.requests, googleapiclient.discovery" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
)

REM Run the Python script
python3 send_email.py

pause