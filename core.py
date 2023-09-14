"""
Core classes to interact with the Umbrella API
Includes authentication, and a base class for the API calls

Usage:
    Import this file into your project

Authentication:
    Uses OAuth2 to get a bearer token

Restrictions:
    Must have generated an API key and secret in the Umbrella dashboard
    Must configure DNS_API_KEY and DNS_API_SECRET as environment variables
    Package list in requirements.txt

To Do:
    Add pagination to the API calls

Author:
    Luke Robertson - September 2023
"""


from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import MissingTokenError
from datetime import datetime
import os
import requests

token_url = 'https://api.umbrella.com/auth/v2/token'


class Auth:
    """A class to authenticate with the Umbrella API

    Attributes
    ----------
    None

    Methods
    -------
    GetToken()
        Get a bearer token from the Umbrella API

    CheckExpiry()
        Check if the existing token has or is about to expire

    """

    def __init__(self):
        """Constructs the class

        Parameters
        ----------
        ident : str
            The client ID for the Umbrella API
        secret : str
            The client secret for the Umbrella API

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # URL for the token endpoint
        self.token_url = 'https://api.umbrella.com/auth/v2/token'

        # Get the client ID and secret from the environment variables
        self.ident = os.environ.get('DNS_API_KEY')
        self.secret = os.environ.get('DNS_API_SECRET')

        if self.ident is None or self.secret is None:
            print("You need to have DNS_API_KEY and DNS_API_SECRET set")
            exit()

        # Initialise the token to None
        self.token = None

        # Initialise the token expiry to now
        self.token_epoch = datetime.now().timestamp()

    def GetToken(self):
        """Gets a bearer token from the Umbrella API

        Stores the token and expiry in the class

        Parameters
        ----------
        None

        Raises
        ------
        MissingTokenError
            If there was a problem with OAuth2

        UmbrellaTokenError
            If there was a problem with the Umbrella API

        Returns
        -------
        None
        """

        # Get the token using OAuth2
        auth = HTTPBasicAuth(self.ident, self.secret)
        client = BackendApplicationClient(client_id=self.ident)
        oauth = OAuth2Session(client=client)

        try:
            token = oauth.fetch_token(token_url=self.token_url, auth=auth)
        except MissingTokenError:
            print("OAuth2 has reported a missing token error")
            print("Check that the client ID and secret are both correct")
            return
        except Exception as e:
            print(f'Error: {e}')

        # Check for a valid response from the API
        if not oauth.authorized:
            raise UmbrellaTokenError("Could not get a token")

        # Store the token in the class
        else:
            self.token = token['access_token']
            self.token_epoch = token['expires_at']

    def CheckExpiry(self):
        """
        Check if the existing token has or is about to expire

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # If the token is about to expire, has expired, or doesn't exist
        # Get a new token
        if datetime.now().timestamp() > (self.token_epoch - 300):
            print("Generating a new API bearer token")
            self.GetToken()

        # Return the remaining time in seconds
        return self.token_epoch - datetime.now().timestamp()


class ApiCall:
    """
    A base class for the API calls
    Other classes will inherit from this

    Attributes
    ----------
    None

    Methods
    -------
    build_params()
        Build a list of parameters to pass to the API

    send_request()
        Build the API request and send it
    """

    def __init__(self, auth, **kwargs):
        """
        Constructs the class

        Sets default parameters such as time range and limit
        Default parameters can be overridden by passing them to init


        Parameters
        ----------
        auth : class
            The auth class, which contains the bearer token

        limit : int
            Set the default limit for the number of results returned

        timefrom : int or string
            Set the default 'from' time for the query

        timeto : int or string
            Set the default 'to' time for the query

        Raises
        ------
        None
        """

        # The base URI
        self.report_uri = 'api.umbrella.com/reports/v2'

        # The auth class
        self.auth = auth

        # Default response limit
        if 'limit' in kwargs:
            self.limit = kwargs['limit']
        else:
            self.limit = 100

        # Default offset for pagination
        self.offset = 0

        # Default time range
        if 'timefrom' in kwargs:
            self.from_date = kwargs['timefrom']
        else:
            self.from_date = '-1days'

        if 'timeto' in kwargs:
            self.to_date = kwargs['timeto']
        else:
            self.to_date = 'now'

        # API headers
        self.headers = {
            'Authorization': 'Bearer ' + self.auth.token,
            'Content-Type': 'application/json'
        }

    # Build a parameter string
    def build_params(self, **kwargs):
        """
        Build a list of parameters to pass to the API
        Includes time range, etc
        Will use defaults if not specified

        Parameters
        ----------
        from : int or string
            Set the default 'from' time for the query

        to : int or string
            Set the default 'to' time for the query

        pagesize : int
            Set the default limit for the number of results returned
            Used for API pagination

        page : int
            The page number to retrieve
            This is the offset for pagination

        Raises
        ------
        None
        """

        # A dictionary of parameters to pass to the API
        params = {}

        # Set the time range
        if 'timefrom' in kwargs:
            params['from'] = kwargs['timefrom']
        else:
            params['from'] = self.from_date

        if 'timeto' in kwargs:
            params['to'] = kwargs['timeto']
        else:
            params['to'] = self.to_date

        # Handle pagination
        if 'size' in kwargs:
            params['limit'] = kwargs['size']
        else:
            params['limit'] = self.limit

        if 'page' in kwargs:
            params['offset'] = kwargs['page']
        else:
            params['offset'] = self.offset

        return params

    # Send a request to the API
    def send_request(self, path, **kwargs):
        """
        Build the API request and send it

        Parameters
        ----------
        path : string
            The path to the API endpoint (excluding the base URI)

        kwargs : dict
            Additional parameters

        Raises
        ------
        None
        """

        # Check the token is valid, and renew if necessary
        self.auth.CheckExpiry()

        # Send the request
        try:
            response = requests.get(
                'https://' + self.report_uri + path,
                headers=self.headers,
                params=self.build_params(**kwargs)
            )

        # Handle errors
        except ConnectionError as e:
            if 'Max retries exceeded' in e:
                print("The API has rejected the request,"
                      "as it's been accessed too many times too quickly.")
            else:
                print(f'A connection error has occurred: {e}')
            return None

        except Exception as e:
            print(f'A generic error has occurred while accessing the API: {e}')
            return None

        # Check the response is ok
        if response.ok:
            return response.json()['data']
        else:
            print(f'Error: API returned status {response.status_code}')
            error = response.json()['data']['errors'][0]
            print(
                f"The \'{error['param']}\' parameter was \'{error['value']}\'"
            )
            print(f"This returned the error \'{error['error']}\'")
            return None


class UmbrellaTokenError(Exception):
    '''
    Exception raised for errors in the Umbrella API
    '''
    pass
