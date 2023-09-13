"""
Connects to Umbrella API and gets a bearer token

Usage:
    Import auth.py
    Run main.py

Authentication:
    Requires OAuth2 to get a bearer token (handled in auth.py)

Restrictions:
    Package list in requirements.txt

To Do:
    All calls should check the token expiry and refresh if necessary

Author:
    Luke Robertson - September 2023
"""


import core
import reports


# Generate the API token
auth_api = core.Auth()
auth_api.GetToken()

# Example call to the reports API
report = reports.Reports(auth_api)
top = report.top_identities(page=2, size=4)
print(top)
